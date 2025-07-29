from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from .birth_certificate_model import BirthCertificate
from .birth_certificate_schemas import BirthCertificateCreate, BirthCertificateRead
from Utility.QRcodeGeneration import QRCodeGeneration
import os
from fastapi.responses import FileResponse
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/birth", response_model=BirthCertificateRead, status_code=status.HTTP_201_CREATED)
def create_birth_certificate(data: BirthCertificateCreate, db: Session = Depends(get_db)):
    # Check for duplicate ID
    if data.id is not None:
        existing = db.query(BirthCertificate).filter(BirthCertificate.id == data.id).first()
        if existing:
            raise HTTPException(status_code=409, detail="A birth certificate with this ID already exists.")
    cert = BirthCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Set barcode to id after save
    barcode_dir = os.path.join("uploaded_images", "birth_certificate_barcodes", str(cert.id))
    os.makedirs(barcode_dir, exist_ok=True)
    barcode_path = os.path.join(barcode_dir, "barcode.png")
    barcode_obj = Code39(
        str(cert.id),
        writer=ImageWriter(),
        add_checksum=False
    )
    barcode_obj.save(
        barcode_path.replace('.png', ''),
        options={
            "write_text": False,
            "module_height": 18,
            "module_width": 1.2,
            "quiet_zone": 6.5
        }
    )
    setattr(cert, "barcode", barcode_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    # --- QR CODE GENERATION ---
    try:
        qr_dir = os.path.join("uploaded_images", "birth_certificates_qr", str(cert.id))
        qr_path = os.path.join(qr_dir, "qrcode.png")
        qr_data = {
            "SRNo": cert.id,
            "Reg Date": str(cert.register_date) if cert.register_date is not None else "",
            "Birth Date": str(cert.birth_date) if cert.birth_date is not None else "",
            "Child Name": cert.child_name_en or "",
            "Sex": cert.gender_en or "",
            "Place Of Birth": cert.birth_place_en or "",
            "Mother Name": cert.mother_name_en or "",
            "Father Name": cert.father_name_en or "",
        }
        QRCodeGeneration.createQRcodeTemp(qr_data, qr_path)
        # --- Save QR path in DB ---
        setattr(cert, "qrcode", qr_path.replace(os.sep, "/"))
        db.commit()
        db.refresh(cert)
    except Exception as e:
        print(f"QR code generation failed: {e}")
    return cert

@router.get("/birth", response_model=list[BirthCertificateRead])
def list_birth_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(BirthCertificate)
    if district_id:
        query = query.filter(BirthCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(BirthCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(BirthCertificate.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get("/birth/{id}", response_model=BirthCertificateRead)
def get_birth_certificate(
    id: int, 
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db), 
    request: Request = None
):
    query = db.query(BirthCertificate).filter(BirthCertificate.id == id)
    if district_id:
        query = query.filter(BirthCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(BirthCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(BirthCertificate.gram_panchayat_id == gram_panchayat_id)
    
    cert = query.first()
    if not cert:
        raise HTTPException(status_code=404, detail="Birth certificate not found")
    cert_data = BirthCertificateRead.from_orm(cert)
    if getattr(cert, "qrcode", None):
        cert_data.qrcode = str(request.base_url)[:-1] + f"/certificates/birth_qrcode/{cert.id}"
    else:
        cert_data.qrcode = None
    # Add barcode_url
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/birth_barcode/{cert.id}"
    return cert_data

@router.put("/birth/{id}", response_model=BirthCertificateRead)
def update_birth_certificate(
    id: int, 
    data: BirthCertificateCreate, 
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(BirthCertificate).filter(BirthCertificate.id == id)
    if district_id:
        query = query.filter(BirthCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(BirthCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(BirthCertificate.gram_panchayat_id == gram_panchayat_id)
    
    cert = query.first()
    if not cert:
        raise HTTPException(status_code=404, detail="Birth certificate not found")
    
    # Update with location fields
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cert, field, value)
    db.commit()
    db.refresh(cert)
    # Regenerate QR code with latest info
    try:
        qr_dir = os.path.join("uploaded_images", "birth_certificates_qr", str(cert.id))
        qr_path = os.path.join(qr_dir, "qrcode.png")
        qr_data = {
            "SRNo": cert.id,
            "Reg Date": str(cert.register_date) if cert.register_date is not None else "",
            "Birth Date": str(cert.birth_date) if cert.birth_date is not None else "",
            "Child Name": cert.child_name_en or "",
            "Sex": cert.gender_en or "",
            "Place Of Birth": cert.birth_place_en or "",
            "Mother Name": cert.mother_name_en or "",
            "Father Name": cert.father_name_en or "",
        }
        QRCodeGeneration.createQRcodeTemp(qr_data, qr_path)
        setattr(cert, "qrcode", qr_path.replace(os.sep, "/"))
        db.commit()
        db.refresh(cert)
    except Exception as e:
        print(f"QR code regeneration failed: {e}")
    return cert

@router.get("/birth_qrcode/{id}")
def get_birth_certificate_qrcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(BirthCertificate).filter(BirthCertificate.id == id).first()
    qr_path = str(getattr(cert, "qrcode", "")) if cert else ""
    if not cert or not qr_path:
        raise HTTPException(status_code=404, detail="QR code not found")
    if not os.path.exists(qr_path):
        raise HTTPException(status_code=404, detail="QR code file not found")
    return FileResponse(qr_path, media_type="image/png")

@router.get("/birth_barcode/{id}")
def get_birth_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(BirthCertificate).filter(BirthCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    from fastapi.responses import FileResponse
    return FileResponse(barcode_path, media_type="image/png") 