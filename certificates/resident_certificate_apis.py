from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .resident_certificate_model import ResidentCertificate
from .resident_certificate_schemas import ResidentCertificateCreate, ResidentCertificateRead
import shutil
import os
from datetime import datetime
from barcode import Code39
from barcode.writer import ImageWriter

router = APIRouter(prefix="/certificates", tags=["certificates"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/resident", response_model=ResidentCertificateRead, status_code=status.HTTP_201_CREATED)
def create_resident_certificate(
    dispatch_no: str = Form(...),
    date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_no: str = Form(...),
    adhar_no_en: str = Form(...),
    image: UploadFile = File(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    db: Session = Depends(get_db)
):
    image_url = None
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    # Create a temp cert to get the id after commit
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    cert = ResidentCertificate(
        dispatch_no=dispatch_no,
        date=date_obj,
        village=village,
        village_en=village_en,
        applicant_name=applicant_name,
        applicant_name_en=applicant_name_en,
        adhar_no=adhar_no,
        adhar_no_en=adhar_no_en,
        district_id=district_id_int,
        taluka_id=taluka_id_int,
        gram_panchayat_id=gram_panchayat_id_int,
        image_url=None,
        barcode=None
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Save image in ResidentCertificates/profiles/{id}/
    if image:
        profile_dir = os.path.join(UPLOAD_DIR, "ResidentCertificates", "profiles", str(cert.id))
        os.makedirs(profile_dir, exist_ok=True)
        safe_filename = image.filename.replace(" ", "_")
        file_path = os.path.join(profile_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        cert.image_url = file_path.replace(os.sep, "/")
        db.commit()
        db.refresh(cert)
    # Generate barcode in ResidentCertificates/barcodes/{id}/
    barcode_dir = os.path.join(UPLOAD_DIR, "ResidentCertificates", "barcodes", str(cert.id))
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
    cert.barcode = barcode_path.replace(os.sep, "/")
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/resident", response_model=list[ResidentCertificateRead])
def list_resident_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(ResidentCertificate)
    if district_id:
        query = query.filter(ResidentCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(ResidentCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(ResidentCertificate.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get("/resident/{id}", response_model=ResidentCertificateRead)
def get_resident_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(ResidentCertificate).filter(ResidentCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Resident certificate not found")
    cert_data = ResidentCertificateRead.from_orm(cert)
    # Add image_url and barcode_url as absolute URLs if present
    if getattr(cert, "image_url", None):
        cert_data.image_url = str(request.base_url)[:-1] + f"/{cert.image_url}" if not cert.image_url.startswith("http") else cert.image_url
    else:
        cert_data.image_url = None
    if getattr(cert, "barcode", None):
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/{cert.barcode}" if not cert.barcode.startswith("http") else cert.barcode
    else:
        cert_data.barcode_url = None
    return cert_data

@router.put("/resident/{id}", response_model=ResidentCertificateRead)
def update_resident_certificate(
    id: int,
    dispatch_no: str = Form(...),
    date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_no: str = Form(...),
    adhar_no_en: str = Form(...),
    image: UploadFile = File(None),
    remove_image: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    db: Session = Depends(get_db)
):
    cert = db.query(ResidentCertificate).filter(ResidentCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Resident certificate not found")
    setattr(cert, "dispatch_no", dispatch_no)
    setattr(cert, "date", datetime.strptime(date, "%Y-%m-%d").date())
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "applicant_name", applicant_name)
    setattr(cert, "applicant_name_en", applicant_name_en)
    setattr(cert, "adhar_no", adhar_no)
    setattr(cert, "adhar_no_en", adhar_no_en)
    # If a new image is uploaded, replace the old image
    if image and image.filename:
        profile_dir = os.path.join(UPLOAD_DIR, "ResidentCertificates", "profiles", str(cert.id))
        os.makedirs(profile_dir, exist_ok=True)
        safe_filename = image.filename.replace(" ", "_")
        file_path = os.path.join(profile_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        setattr(cert, "image_url", file_path.replace(os.sep, "/"))
    # If remove_image is true, delete the image file and clear image_url
    if remove_image and remove_image.lower() == "true":
        if cert.image_url and os.path.exists(cert.image_url):
            try:
                os.remove(cert.image_url)
            except Exception:
                pass
        setattr(cert, "image_url", None)
    db.commit()
    db.refresh(cert)
    return cert 