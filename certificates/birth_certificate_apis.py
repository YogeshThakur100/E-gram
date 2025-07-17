from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from .birth_certificate_model import BirthCertificate
from .birth_certificate_schemas import BirthCertificateCreate, BirthCertificateRead
from Utility.QRcodeGeneration import QRCodeGeneration
import os

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/birth", response_model=BirthCertificateRead, status_code=status.HTTP_201_CREATED)
def create_birth_certificate(data: BirthCertificateCreate, db: Session = Depends(get_db)):
    # Check for duplicate ID
    if data.id is not None:
        existing = db.query(BirthCertificate).filter(BirthCertificate.id == data.id).first()
        if existing:
            raise HTTPException(status_code=409, detail="A birth certificate with this ID already exists.")
    cert = BirthCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # --- QR CODE GENERATION ---
    try:
        qr_dir = os.path.join("uploaded_images", "birth_certificates_qr", str(cert.id))
        qr_path = os.path.join(qr_dir, "qrcode.png")
        qr_data = {
            "SRNo": cert.id,
            "Reg Date": str(cert.register_date) if cert.register_date is not None else "",
            "Birth Date": str(cert.birth_date) if cert.birth_date is not None else "",
            "Child Name": cert.child_name_en or "",
            "Sex": cert.gender_en or "",
            "Place Of Birth": cert.birth_place_en or "",
            "Mother Name": cert.mother_name_en or "",
            "Father Name": cert.father_name_en or "",
        }
        QRCodeGeneration.createQRcodeTemp(qr_data, qr_path)
    except Exception as e:
        print(f"QR code generation failed: {e}")
    return cert

@router.get("/birth", response_model=list[BirthCertificateRead])
def list_birth_certificates(db: Session = Depends(get_db)):
    return db.query(BirthCertificate).all() 