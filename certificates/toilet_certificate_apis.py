from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from database import get_db
from .toilet_certificate_model import ToiletCertificate
from .toilet_certificate_schemas import ToiletCertificateCreate, ToiletCertificateRead
from datetime import datetime

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/toilet", response_model=ToiletCertificateRead, status_code=status.HTTP_201_CREATED)
def create_toilet_certificate(
    registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    applicant_name: str = Form(None),
    applicant_name_en: str = Form(None),
    adhar_number: str = Form(None),
    adhar_number_en: str = Form(None),
    db: Session = Depends(get_db)
):
    # Convert registration_date string to date object
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    cert = ToiletCertificate(
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
    return cert

@router.get("/toilet", response_model=list[ToiletCertificateRead])
def list_toilet_certificates(db: Session = Depends(get_db)):
    return db.query(ToiletCertificate).all() 