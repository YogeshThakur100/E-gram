from fastapi import APIRouter, Depends, status, Form, HTTPException, Request
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session
from database import get_db
from .receipt_certificate_model import ReceiptCertificate
from .receipt_certificate_schemas import ReceiptCertificateCreate, ReceiptCertificateRead
from datetime import datetime
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/receipt", response_model=ReceiptCertificateRead, status_code=status.HTTP_201_CREATED)
def create_receipt_certificate(
    receipt_date: str = Form(...),
    receipt_id: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    name1: str = Form(None),
    name1_en: str = Form(None),
    name2: str = Form(None),
    name2_en: str = Form(None),
    receipt_amount: str = Form(None),
    receipt_amount_en: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    db: Session = Depends(get_db)
):
    date_obj = datetime.strptime(receipt_date, "%Y-%m-%d").date()
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    cert = ReceiptCertificate(
        receipt_date=date_obj,
        receipt_id=receipt_id,
        village=village,
        village_en=village_en,
        name1=name1,
        name1_en=name1_en,
        name2=name2,
        name2_en=name2_en,
        receipt_amount=receipt_amount,
        receipt_amount_en=receipt_amount_en,
        district_id=district_id_int,
        taluka_id=taluka_id_int,
        gram_panchayat_id=gram_panchayat_id_int
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Generate and save barcode image
    barcode_dir = os.path.join("uploaded_images", "receipt_certificates", str(cert.id))
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
    return cert

@router.get("/receipt", response_model=list[ReceiptCertificateRead])
def list_receipt_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    query = db.query(ReceiptCertificate)
    if district_id:
        query = query.filter(ReceiptCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(ReceiptCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(ReceiptCertificate.gram_panchayat_id == gram_panchayat_id)
    certs = query.all()
    result = []
    for cert in certs:
        cert_data = ReceiptCertificateRead.from_orm(cert)
        barcode_val = str(getattr(cert, 'barcode', ''))
        if barcode_val:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
        else:
            cert_data.barcode_url = None
        cert_data.gramPanchayat = None
        cert_data.taluka = None
        cert_data.jilha = None
        result.append(cert_data)
    return result

@router.get("/receipt/{id}", response_model=ReceiptCertificateRead)
def get_receipt_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Receipt certificate not found")
    cert_data = ReceiptCertificateRead.from_orm(cert)
    barcode_val = str(getattr(cert, 'barcode', ''))
    if barcode_val:
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
    else:
        cert_data.barcode_url = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/receipt/{id}", response_model=ReceiptCertificateRead)
def update_receipt_certificate(id: int, receipt_date: str = Form(...),
    receipt_id: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    name1: str = Form(None),
    name1_en: str = Form(None),
    name2: str = Form(None),
    name2_en: str = Form(None),
    receipt_amount: str = Form(None),
    receipt_amount_en: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    db: Session = Depends(get_db)):
    cert = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Receipt certificate not found")
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    date_obj = datetime.strptime(receipt_date, "%Y-%m-%d").date()
    setattr(cert, "receipt_date", date_obj)
    setattr(cert, "receipt_id", receipt_id)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "name1", name1)
    setattr(cert, "name1_en", name1_en)
    setattr(cert, "name2", name2)
    setattr(cert, "name2_en", name2_en)
    setattr(cert, "receipt_amount", receipt_amount)
    setattr(cert, "receipt_amount_en", receipt_amount_en)
    setattr(cert, "district_id", district_id_int)
    setattr(cert, "taluka_id", taluka_id_int)
    setattr(cert, "gram_panchayat_id", gram_panchayat_id_int)
    # Regenerate barcode
    barcode_dir = os.path.join("uploaded_images", "receipt_certificates", str(cert.id))
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
    return cert

@router.get("/receipt_barcode/{id}")
def get_receipt_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    return FileResponse(barcode_path, media_type="image/png") 