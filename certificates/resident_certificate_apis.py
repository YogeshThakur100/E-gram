from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from .resident_certificate_model import ResidentCertificate
from .resident_certificate_schemas import ResidentCertificateCreate, ResidentCertificateRead
import shutil
import os
from datetime import datetime

router = APIRouter(prefix="/certificates", tags=["certificates"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/resident", response_model=ResidentCertificateRead, status_code=status.HTTP_201_CREATED)
def create_resident_certificate(
    dispatch_no: str = Form(...),
    date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_no: str = Form(...),
    adhar_no_en: str = Form(...),
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
    # Convert date string to date object
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    cert = ResidentCertificate(
        dispatch_no=dispatch_no,
        date=date_obj,
        village=village,
        village_en=village_en,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        adhar_no=adhar_no,
        adhar_no_en=adhar_no_en,
        image_url=image_url
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/resident", response_model=list[ResidentCertificateRead])
def list_resident_certificates(db: Session = Depends(get_db)):
    return db.query(ResidentCertificate).all() 