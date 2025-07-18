from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .death_certificate_model import DeathCertificate
from .death_certificate_schemas import DeathCertificateCreate, DeathCertificateRead
from Utility.QRcodeGeneration import QRCodeGeneration
import os
from fastapi.responses import FileResponse
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/death", response_model=DeathCertificateRead, status_code=status.HTTP_201_CREATED)
def create_death_certificate(data: DeathCertificateCreate, db: Session = Depends(get_db)):
    cert = DeathCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Set barcode to id after save
    barcode_dir = os.path.join("uploaded_images", "death_certificate_barcodes", str(cert.id))
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
        qr_dir = os.path.join("uploaded_images", "death_certificates_qr", str(cert.id))
        qr_path = os.path.join(qr_dir, "qrcode.png")
        qr_data = {
            "SRNo": cert.id,
            "Reg Date": str(cert.register_date) if cert.register_date is not None else "",
            "Death Date": str(cert.death_date) if cert.death_date is not None else "",
            "Name": cert.deceased_name_en or cert.deceased_name or "",
            "Gender": cert.gender or "",
            "Gender (EN)": cert.gender_en or "",
            "Place Of Death": cert.place_of_death_en or cert.place_of_death or "",
            "Mother Name": cert.mother_name_en or cert.mother_name or "",
            "Father Name": cert.father_name_en or cert.father_name or "",
        }
        QRCodeGeneration.createQRcodeTemp(qr_data, qr_path)
        setattr(cert, "qrcode", qr_path.replace(os.sep, "/"))
        db.commit()
        db.refresh(cert)
    except Exception as e:
        print(f"QR code generation failed: {e}")
    return cert

@router.get("/death", response_model=list[DeathCertificateRead])
def list_death_certificates(db: Session = Depends(get_db)):
    return db.query(DeathCertificate).all()

@router.get("/death/{id}", response_model=DeathCertificateRead)
def get_death_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(DeathCertificate).filter(DeathCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Death certificate not found")
    cert_data = DeathCertificateRead.from_orm(cert)
    if getattr(cert, "qrcode", None):
        cert_data.qrcode = str(request.base_url)[:-1] + f"/certificates/death_qrcode/{cert.id}"
    else:
        cert_data.qrcode = None
    # Add barcode_url
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/death_barcode/{cert.id}"
    return cert_data

@router.get("/death_qrcode/{id}")
def get_death_certificate_qrcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(DeathCertificate).filter(DeathCertificate.id == id).first()
    qr_path = str(getattr(cert, "qrcode", "")) if cert else ""
    if not cert or not qr_path:
        raise HTTPException(status_code=404, detail="QR code not found")
    if not os.path.exists(qr_path):
        raise HTTPException(status_code=404, detail="QR code file not found")
    return FileResponse(qr_path, media_type="image/png")

@router.get("/death_barcode/{id}")
def get_death_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(DeathCertificate).filter(DeathCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    from fastapi.responses import FileResponse
    return FileResponse(barcode_path, media_type="image/png") 