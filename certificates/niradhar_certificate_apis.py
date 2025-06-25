from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from database import get_db
from .niradhar_certificate_model import NiradharCertificate
from .niradhar_certificate_schemas import NiradharCertificateCreate, NiradharCertificateRead
from datetime import datetime

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/niradhar", response_model=NiradharCertificateRead, status_code=status.HTTP_201_CREATED)
def create_niradhar_certificate(
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
    cert = NiradharCertificate(
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

@router.get("/niradhar", response_model=list[NiradharCertificateRead])
def list_niradhar_certificates(db: Session = Depends(get_db)):
    return db.query(NiradharCertificate).all() 