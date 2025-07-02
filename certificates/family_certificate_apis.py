from fastapi import APIRouter, Depends, status, Form
from sqlalchemy.orm import Session
from database import get_db
from .family_certificate_model import FamilyCertificate
from .family_certificate_schemas import FamilyCertificateCreate, FamilyCertificateRead
from datetime import datetime

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
    relation_type: str = Form(None),
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
        relation_type=relation_type
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/family", response_model=list[FamilyCertificateRead])
def list_family_certificates(db: Session = Depends(get_db)):
    return db.query(FamilyCertificate).all() 