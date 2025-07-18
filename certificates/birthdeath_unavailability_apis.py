from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .birthdeath_unavailability_model import BirthDeathUnavailabilityCertificate
from .birthdeath_unavailability_schemas import BirthDeathUnavailabilityCertificateCreate, BirthDeathUnavailabilityCertificateRead
import os
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/birthdeath-unavailability", response_model=BirthDeathUnavailabilityCertificateRead, status_code=status.HTTP_201_CREATED)
def create_certificate(data: BirthDeathUnavailabilityCertificateCreate, db: Session = Depends(get_db)):
    cert = BirthDeathUnavailabilityCertificate(**data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Generate and save barcode image
    barcode_dir = os.path.join("uploaded_images", "birthdeath_unavailability_barcodes", str(cert.id))
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
            "write_text": False,      # No number below barcode
            "module_height": 18,     # Shorter bars, like original
            "module_width": 1.2,     # Wider barcode, like original
            "quiet_zone": 6.5        # Standard margin
        }
    )
    # Store barcode image path in DB
    setattr(cert, "barcode", barcode_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/birthdeath-unavailability", response_model=list[BirthDeathUnavailabilityCertificateRead])
def list_certificates(db: Session = Depends(get_db)):
    return db.query(BirthDeathUnavailabilityCertificate).all()

@router.get("/birthdeath-unavailability/{id}", response_model=BirthDeathUnavailabilityCertificateRead)
def get_birthdeath_unavailability_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(BirthDeathUnavailabilityCertificate).filter(BirthDeathUnavailabilityCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    cert_data = BirthDeathUnavailabilityCertificateRead.from_orm(cert)
    # Add barcode_url
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/birthdeath-unavailability_barcode/{cert.id}"
    return cert_data

@router.put("/birthdeath-unavailability/{id}", response_model=BirthDeathUnavailabilityCertificateRead)
def update_birthdeath_unavailability_certificate(id: int, data: BirthDeathUnavailabilityCertificateCreate, db: Session = Depends(get_db)):
    cert = db.query(BirthDeathUnavailabilityCertificate).filter(BirthDeathUnavailabilityCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    for field, value in data.dict(exclude_unset=True).items():
        setattr(cert, field, value)
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/birthdeath-unavailability_barcode/{id}")
def get_birthdeath_unavailability_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(BirthDeathUnavailabilityCertificate).filter(BirthDeathUnavailabilityCertificate.id == id).first()
    if not cert or not getattr(cert, 'barcode', None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, 'barcode', None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    from fastapi.responses import FileResponse
    return FileResponse(barcode_path, media_type="image/png") 