from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from .no_benefit_certificate_model import NoBenefitCertificate
from .no_benefit_certificate_schemas import NoBenefitCertificateCreate, NoBenefitCertificateRead
from datetime import datetime
import shutil
import os
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/no-benefit", response_model=NoBenefitCertificateRead, status_code=status.HTTP_201_CREATED)
def create_no_benefit_certificate(
    registration_date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_number: str = Form(...),
    adhar_number_en: str = Form(...),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    # Create cert first to get ID
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    cert = NoBenefitCertificate(
        registration_date=reg_date_obj,
        village=village,
        village_en=village_en,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        adhar_number=adhar_number,
        adhar_number_en=adhar_number_en,
        district_id=district_id_int,
        taluka_id=taluka_id_int,
        gram_panchayat_id=gram_panchayat_id_int,
        image_url=None
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Save image if present
    if image:
        safe_filename = image.filename.replace(' ', '_')
        image_dir = os.path.join(UPLOAD_DIR, "nobenefit", "profiles", str(cert.id))
        os.makedirs(image_dir, exist_ok=True)
        file_path = os.path.join(image_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = file_path.replace(os.sep, "/")
        setattr(cert, "image_url", image_url)
        db.commit()
        db.refresh(cert)
    # Generate and save barcode image
    barcode_dir = os.path.join(UPLOAD_DIR, "nobenefit", "barcodes", str(cert.id))
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

@router.get("/no-benefit", response_model=list[NoBenefitCertificateRead])
def list_no_benefit_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(NoBenefitCertificate)
    if district_id:
        query = query.filter(NoBenefitCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(NoBenefitCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(NoBenefitCertificate.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get("/no-benefit/{id}", response_model=NoBenefitCertificateRead)
def get_no_benefit_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="No Benefit certificate not found")
    cert_data = NoBenefitCertificateRead.from_orm(cert)
    # Add barcode_url
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}"
    # Add image_url as absolute URL if present
    image_url_val = getattr(cert, 'image_url', None)
    if image_url_val and isinstance(image_url_val, str):
        if image_url_val.startswith("http"):
            cert_data.image_url = image_url_val
        else:
            cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
    else:
        cert_data.image_url = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/no-benefit/{id}", response_model=NoBenefitCertificateRead)
def update_no_benefit_certificate(
    id: int,
    request: Request,
    registration_date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_number: str = Form(...),
    adhar_number_en: str = Form(...),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    image: UploadFile = File(None),
    remove_image: bool = Form(False),
    db: Session = Depends(get_db)
):
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="No Benefit certificate not found")
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    setattr(cert, "registration_date", reg_date_obj)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "applicant_name", applicant_name)
    setattr(cert, "applicant_name_en", applicant_name_en)
    setattr(cert, "adhar_number", adhar_number)
    setattr(cert, "adhar_number_en", adhar_number_en)
    setattr(cert, "district_id", district_id_int)
    setattr(cert, "taluka_id", taluka_id_int)
    setattr(cert, "gram_panchayat_id", gram_panchayat_id_int)
    # Handle image update/removal
    if remove_image and cert.image_url:
        try:
            os.remove(cert.image_url)
        except Exception:
            pass
        setattr(cert, "image_url", None)
    elif image:
        safe_filename = image.filename.replace(' ', '_')
        image_dir = os.path.join(UPLOAD_DIR, "nobenefit", "profiles", str(cert.id))
        os.makedirs(image_dir, exist_ok=True)
        file_path = os.path.join(image_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        setattr(cert, "image_url", file_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    # Regenerate barcode
    barcode_dir = os.path.join(UPLOAD_DIR, "nobenefit", "barcodes", str(cert.id))
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
    # Return with absolute URLs
    cert_data = NoBenefitCertificateRead.from_orm(cert)
    cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}"
    image_url_val = getattr(cert, 'image_url', None)
    if image_url_val and isinstance(image_url_val, str):
        if image_url_val.startswith("http"):
            cert_data.image_url = image_url_val
        else:
            cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
    else:
        cert_data.image_url = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.get("/no_benefit_barcode/{id}")
def get_no_benefit_certificate_barcode(id: int, db: Session = Depends(get_db)):
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert or not getattr(cert, "barcode", None):
        raise HTTPException(status_code=404, detail="Barcode not found")
    barcode_path = getattr(cert, "barcode", None)
    if not barcode_path or not os.path.exists(barcode_path):
        raise HTTPException(status_code=404, detail="Barcode file not found")
    return FileResponse(barcode_path, media_type="image/png") 