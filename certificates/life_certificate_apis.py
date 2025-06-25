from fastapi import APIRouter, Depends, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from .life_certificate_model import LifeCertificate
from .life_certificate_schemas import LifeCertificateCreate, LifeCertificateRead
from datetime import datetime
import shutil
import os

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
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    if image:
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = file_path
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    cert = LifeCertificate(
        registration_date=reg_date_obj,
        village=village,
        village_en=village_en,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        adhar_number=adhar_number,
        adhar_number_en=adhar_number_en,
        image_url=image_url
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/life", response_model=list[LifeCertificateRead])
def list_life_certificates(db: Session = Depends(get_db)):
    return db.query(LifeCertificate).all() 