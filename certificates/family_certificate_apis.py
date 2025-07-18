from fastapi import APIRouter, Depends, status, Form, HTTPException, Request
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session
from database import get_db
from .family_certificate_model import FamilyCertificate
from .family_certificate_schemas import FamilyCertificateCreate, FamilyCertificateRead
from datetime import datetime
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/family", response_model=FamilyCertificateRead, status_code=status.HTTP_201_CREATED)
def create_family_certificate(
    registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    family_name: str = Form(None),
    family_name_en: str = Form(None),
    adhar_number: str = Form(None),
    adhar_number_en: str = Form(None),
    record_no: str = Form(None),
    applicant_name: str = Form(None),
    applicant_name_en: str = Form(None),
    relation: str = Form(None),
    relation_en: str = Form(None),
    year: str = Form(None),
    db: Session = Depends(get_db)
):
    # Convert registration_date string to date object
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    cert = FamilyCertificate(
        registration_date=reg_date_obj,
        village=village,
        village_en=village_en,
        family_name=family_name,
        family_name_en=family_name_en,
        adhar_number=adhar_number,
        adhar_number_en=adhar_number_en,
        record_no=record_no,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        relation=relation,
        relation_en=relation_en,
        year=year
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Generate and save barcode image
    barcode_dir = os.path.join("uploaded_images", "family_certificate_barcodes", str(cert.id))
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

@router.get("/family", response_model=list[FamilyCertificateRead])
def list_family_certificates(db: Session = Depends(get_db)):
    return db.query(FamilyCertificate).all() 

@router.get("/family/{id}", response_model=FamilyCertificateRead)
def get_family_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(FamilyCertificate).filter(FamilyCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Family certificate not found")
    cert_data = FamilyCertificateRead.from_orm(cert)
    # Add barcode_url
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/family_barcode/{cert.id}"
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/family/{id}", response_model=FamilyCertificateRead)
def update_family_certificate(id: int, registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    family_name: str = Form(None),
    family_name_en: str = Form(None),
    adhar_number: str = Form(None),
    adhar_number_en: str = Form(None),
    record_no: str = Form(None),
    applicant_name: str = Form(None),
    applicant_name_en: str = Form(None),
    relation: str = Form(None),
    relation_en: str = Form(None),
    year: str = Form(None),
    db: Session = Depends(get_db)):
    cert = db.query(FamilyCertificate).filter(FamilyCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Family certificate not found")
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    setattr(cert, "registration_date", reg_date_obj)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "family_name", family_name)
    setattr(cert, "family_name_en", family_name_en)
    setattr(cert, "adhar_number", adhar_number)
    setattr(cert, "adhar_number_en", adhar_number_en)
    setattr(cert, "record_no", record_no)
    setattr(cert, "applicant_name", applicant_name)
    setattr(cert, "applicant_name_en", applicant_name_en)
    setattr(cert, "relation", relation)
    setattr(cert, "relation_en", relation_en)
    setattr(cert, "year", year)
    db.commit()
    db.refresh(cert)
    # Regenerate barcode
    barcode_dir = os.path.join("uploaded_images", "family_certificate_barcodes", str(cert.id))
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

@router.get("/family_barcode/{id}")
def get_family_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(FamilyCertificate).filter(FamilyCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    return FileResponse(barcode_path, media_type="image/png") 