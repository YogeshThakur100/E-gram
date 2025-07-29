from fastapi import APIRouter, Depends, status, Form, HTTPException, Request, File, UploadFile
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session
from database import get_db
from .unemployment_certificate_model import UnemploymentCertificate
from .unemployment_certificate_schemas import UnemploymentCertificateCreate, UnemploymentCertificateRead
from datetime import datetime
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/unemployment", response_model=UnemploymentCertificateRead, status_code=status.HTTP_201_CREATED)
def create_unemployment_certificate(
    registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    applicant_name: str = Form(None),
    applicant_name_en: str = Form(None),
    adhar_number: str = Form(None),
    adhar_number_en: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Convert empty strings to None for location fields
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    cert = UnemploymentCertificate(
        registration_date=reg_date_obj,
        village=village,
        village_en=village_en,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        adhar_number=adhar_number,
        adhar_number_en=adhar_number_en,
        district_id=district_id_int,
        taluka_id=taluka_id_int,
        gram_panchayat_id=gram_panchayat_id_int
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Handle image upload
    image_path = None
    if image:
        filename = image.filename.replace(" ", "_") if image.filename else "image.png"
        image_dir = os.path.join("uploaded_images", "unemployment_certificates", str(cert.id))
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, filename)
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        setattr(cert, "image", image_path.replace(os.sep, "/"))
    # Generate and save barcode image
    barcode_dir = os.path.join("uploaded_images", "unemployment_certificates", str(cert.id))
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
            "write_text": False,
            "module_height": 18,
            "module_width": 1.2,
            "quiet_zone": 6.5
        }
    )
    setattr(cert, "barcode", barcode_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/unemployment", response_model=list[UnemploymentCertificateRead])
def list_unemployment_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    request: Request = None, 
    db: Session = Depends(get_db)
):
    query = db.query(UnemploymentCertificate)
    
    # Apply location filters if provided
    if district_id:
        query = query.filter(UnemploymentCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(UnemploymentCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(UnemploymentCertificate.gram_panchayat_id == gram_panchayat_id)
    
    certs = query.all()
    result = []
    for cert in certs:
        cert_data = UnemploymentCertificateRead.from_orm(cert)
        # Absolute URLs
        barcode_val = str(getattr(cert, 'barcode', ''))
        if barcode_val:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
        else:
            cert_data.barcode_url = None
        image_val = str(getattr(cert, 'image', ''))
        if image_val:
            cert_data.image_url = str(request.base_url)[:-1] + f"/{image_val}" if not image_val.startswith("http") else image_val
        else:
            cert_data.image_url = None
        cert_data.gramPanchayat = None
        cert_data.taluka = None
        cert_data.jilha = None
        result.append(cert_data)
    return result

@router.get("/unemployment/{id}", response_model=UnemploymentCertificateRead)
def get_unemployment_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(UnemploymentCertificate).filter(UnemploymentCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Unemployment certificate not found")
    cert_data = UnemploymentCertificateRead.from_orm(cert)
    barcode_val = str(getattr(cert, 'barcode', ''))
    if barcode_val:
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
    else:
        cert_data.barcode_url = None
    image_val = str(getattr(cert, 'image', ''))
    if image_val:
        cert_data.image_url = str(request.base_url)[:-1] + f"/{image_val}" if not image_val.startswith("http") else image_val
    else:
        cert_data.image_url = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/unemployment/{id}", response_model=UnemploymentCertificateRead)
def update_unemployment_certificate(id: int, registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    applicant_name: str = Form(None),
    applicant_name_en: str = Form(None),
    adhar_number: str = Form(None),
    adhar_number_en: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)):
    cert = db.query(UnemploymentCertificate).filter(UnemploymentCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Unemployment certificate not found")
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    setattr(cert, "registration_date", reg_date_obj)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "applicant_name", applicant_name)
    setattr(cert, "applicant_name_en", applicant_name_en)
    setattr(cert, "adhar_number", adhar_number)
    setattr(cert, "adhar_number_en", adhar_number_en)
    setattr(cert, "district_id", int(district_id) if district_id and district_id.strip() else None)
    setattr(cert, "taluka_id", int(taluka_id) if taluka_id and taluka_id.strip() else None)
    setattr(cert, "gram_panchayat_id", int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None)
    # Handle image upload and removal
    image_dir = os.path.join("uploaded_images", "unemployment_certificates", str(cert.id))
    os.makedirs(image_dir, exist_ok=True)
    old_image_path = getattr(cert, "image", None)
    if image:
        filename = image.filename.replace(" ", "_") if image.filename else "image.png"
        image_path = os.path.join(image_dir, filename)
        # Remove old image if exists and is different
        if old_image_path and os.path.exists(old_image_path) and old_image_path != image_path:
            try:
                os.remove(old_image_path)
            except Exception:
                pass
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        setattr(cert, "image", image_path.replace(os.sep, "/"))
    else:
        # If no image provided, remove old image and clear DB field
        if old_image_path and os.path.exists(old_image_path):
            try:
                os.remove(old_image_path)
            except Exception:
                pass
        setattr(cert, "image", None)
    # Regenerate barcode
    barcode_dir = os.path.join("uploaded_images", "unemployment_certificates", str(cert.id))
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
            "write_text": False,
            "module_height": 18,
            "module_width": 1.2,
            "quiet_zone": 6.5
        }
    )
    setattr(cert, "barcode", barcode_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/unemployment_barcode/{id}")
def get_unemployment_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(UnemploymentCertificate).filter(UnemploymentCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    return FileResponse(barcode_path, media_type="image/png")

@router.get("/unemployment_image/{id}")
def get_unemployment_certificate_image(id: int, db: Session = Depends(get_db)):
    cert = db.query(UnemploymentCertificate).filter(UnemploymentCertificate.id == id).first()
    if not cert or not getattr(cert, "image", None):
        raise HTTPException(status_code=404, detail="Image not found")
    image_path = getattr(cert, "image", None)
    if not image_path or not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image file not found")
    return FileResponse(image_path, media_type="image/png") 