from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from .death_certificate_model import DeathCertificate
from .death_certificate_schemas import DeathCertificateCreate, DeathCertificateRead

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/death", response_model=DeathCertificateRead, status_code=status.HTTP_201_CREATED)
def create_death_certificate(data: DeathCertificateCreate, db: Session = Depends(get_db)):
    cert = DeathCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/death", response_model=list[DeathCertificateRead])
def list_death_certificates(db: Session = Depends(get_db)):
    return db.query(DeathCertificate).all() 