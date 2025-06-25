from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from .birthdeath_unavailability_model import BirthDeathUnavailabilityCertificate
from .birthdeath_unavailability_schemas import BirthDeathUnavailabilityCertificateCreate, BirthDeathUnavailabilityCertificateRead

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/birthdeath-unavailability", response_model=BirthDeathUnavailabilityCertificateRead, status_code=status.HTTP_201_CREATED)
def create_certificate(data: BirthDeathUnavailabilityCertificateCreate, db: Session = Depends(get_db)):
    cert = BirthDeathUnavailabilityCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/birthdeath-unavailability", response_model=list[BirthDeathUnavailabilityCertificateRead])
def list_certificates(db: Session = Depends(get_db)):
    return db.query(BirthDeathUnavailabilityCertificate).all() 