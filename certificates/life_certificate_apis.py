from fastapi import APIRouter, Depends, status, Form, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from .life_certificate_model import LifeCertificate
from .life_certificate_schemas import LifeCertificateCreate, LifeCertificateRead
from datetime import datetime
import shutil
import os
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/life", response_model=LifeCertificateRead, status_code=status.HTTP_201_CREATED)
def create_life_certificate(
    registration_date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_number: str = Form(...),
    adhar_number_en: str = Form(...),
    db: Session = Depends(get_db)
):
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    cert = LifeCertificate(
        registration_date=reg_date_obj,
        village=village,
        village_en=village_en,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        adhar_number=adhar_number,
        adhar_number_en=adhar_number_en
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Generate and save barcode image in uploaded_images/life_certificate_barcodes/{id}/barcode.png
    barcode_dir = os.path.join("uploaded_images", "life_certificate_barcodes", str(cert.id))
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

@router.get("/life", response_model=list[LifeCertificateRead])
def list_life_certificates(db: Session = Depends(get_db)):
    return db.query(LifeCertificate).all()

@router.get("/life/{id}", response_model=LifeCertificateRead)
def get_life_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(LifeCertificate).filter(LifeCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Life certificate not found")
    cert_data = LifeCertificateRead.from_orm(cert)
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/life_barcode/{cert.id}"
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/life/{id}", response_model=LifeCertificateRead)
def update_life_certificate(
    id: int,
    request: Request,
    registration_date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_number: str = Form(...),
    adhar_number_en: str = Form(...),
    db: Session = Depends(get_db)
):
    cert = db.query(LifeCertificate).filter(LifeCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Life certificate not found")
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    setattr(cert, "registration_date", reg_date_obj)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "applicant_name", applicant_name)
    setattr(cert, "applicant_name_en", applicant_name_en)
    setattr(cert, "adhar_number", adhar_number)
    setattr(cert, "adhar_number_en", adhar_number_en)
    db.commit()
    db.refresh(cert)
    # Regenerate barcode
    barcode_dir = os.path.join("uploaded_images", "life_certificate_barcodes", str(cert.id))
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
    cert_data = LifeCertificateRead.from_orm(cert)
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/life_barcode/{cert.id}"
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.get("/life_barcode/{id}")
def get_life_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(LifeCertificate).filter(LifeCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    return FileResponse(barcode_path, media_type="image/png") 