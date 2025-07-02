from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from .birth_certificate_model import BirthCertificate
from .birth_certificate_schemas import BirthCertificateCreate, BirthCertificateRead

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/birth", response_model=BirthCertificateRead, status_code=status.HTTP_201_CREATED)
def create_birth_certificate(data: BirthCertificateCreate, db: Session = Depends(get_db)):
    cert = BirthCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/birth", response_model=list[BirthCertificateRead])
def list_birth_certificates(db: Session = Depends(get_db)):
    return db.query(BirthCertificate).all() 