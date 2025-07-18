from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .good_conduct_certificate_model import GoodConductCertificate
from .good_conduct_certificate_schemas import GoodConductCertificateCreate, GoodConductCertificateRead
from datetime import datetime
import shutil
import os
from fastapi import Request

router = APIRouter(prefix="/certificates", tags=["certificates"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/good-conduct", response_model=GoodConductCertificateRead, status_code=status.HTTP_201_CREATED)
def create_good_conduct_certificate(
    registration_date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_number: str = Form(...),
    adhar_number_en: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None
    cert = None
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    if image:
        safe_filename = image.filename.replace(' ', '_')
        # Temporarily create cert to get ID after commit
        cert = GoodConductCertificate(
            registration_date=reg_date_obj,
            village=village,
            village_en=village_en,
            applicant_name=applicant_name,
            applicant_name_en=applicant_name_en,
            adhar_number=adhar_number,
            adhar_number_en=adhar_number_en,
            image_url=None
        )
        db.add(cert)
        db.commit()
        db.refresh(cert)
        image_dir = os.path.join(UPLOAD_DIR, "goodconduct", "profiles", str(cert.id))
        os.makedirs(image_dir, exist_ok=True)
        file_path = os.path.join(image_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        if file_path is not None:
            image_url = file_path.replace(os.sep, "/")
            setattr(cert, "image_url", image_url)
            db.commit()
            db.refresh(cert)
    else:
        cert = GoodConductCertificate(
            registration_date=reg_date_obj,
            village=village,
            village_en=village_en,
            applicant_name=applicant_name,
            applicant_name_en=applicant_name_en,
            adhar_number=adhar_number,
            adhar_number_en=adhar_number_en,
            image_url=None
        )
        db.add(cert)
        db.commit()
        db.refresh(cert)
    # Generate and save barcode image
    barcode_dir = os.path.join(UPLOAD_DIR, "good_conduct_certificate_barcodes", str(cert.id))
    os.makedirs(barcode_dir, exist_ok=True)
    barcode_path = os.path.join(barcode_dir, "barcode.png")
    from barcode import Code39
    from barcode.writer import ImageWriter
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

@router.get("/good-conduct", response_model=list[GoodConductCertificateRead])
def list_good_conduct_certificates(request: Request, db: Session = Depends(get_db)):
    certs = db.query(GoodConductCertificate).all()
    result = []
    for cert in certs:
        cert_data = GoodConductCertificateRead.from_orm(cert)
        image_url_val = getattr(cert, 'image_url', None)
        if image_url_val:
            if str(image_url_val).startswith("http"):
                cert_data.image_url = image_url_val
            else:
                cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
        else:
            cert_data.image_url = None
        barcode_val = getattr(cert, 'barcode', None)
        if barcode_val:
            if str(barcode_val).startswith("http"):
                cert_data.barcode = barcode_val
            else:
                cert_data.barcode = str(request.base_url)[:-1] + f"/{barcode_val}"
        else:
            cert_data.barcode = None
        cert_data.gramPanchayat = None
        cert_data.taluka = None
        cert_data.jilha = None
        result.append(cert_data)
    return result

@router.put("/good-conduct/{id}", response_model=GoodConductCertificateRead)
def update_good_conduct_certificate(id: int,
    registration_date: str = Form(...),
    village: str = Form(...),
    village_en: str = Form(...),
    applicant_name: str = Form(...),
    applicant_name_en: str = Form(...),
    adhar_number: str = Form(...),
    adhar_number_en: str = Form(...),
    image: UploadFile = File(None),
    remove_image: bool = Form(False),
    db: Session = Depends(get_db)):
    cert = db.query(GoodConductCertificate).filter(GoodConductCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Good Conduct certificate not found")
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    setattr(cert, "registration_date", reg_date_obj)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "applicant_name", applicant_name)
    setattr(cert, "applicant_name_en", applicant_name_en)
    setattr(cert, "adhar_number", adhar_number)
    setattr(cert, "adhar_number_en", adhar_number_en)
    # Handle image update/removal
    UPLOAD_DIR = "uploaded_images"
    if remove_image and getattr(cert, 'image_url', None):
        try:
            os.remove(getattr(cert, 'image_url'))
        except Exception:
            pass
        setattr(cert, 'image_url', None)
    elif image:
        safe_filename = image.filename.replace(' ', '_')
        image_dir = os.path.join(UPLOAD_DIR, "goodconduct", "profiles", str(cert.id))
        os.makedirs(image_dir, exist_ok=True)
        file_path = os.path.join(image_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        if file_path is not None:
            image_url = file_path.replace(os.sep, "/")
            setattr(cert, "image_url", image_url)
    db.commit()
    db.refresh(cert)
    # Regenerate barcode
    barcode_dir = os.path.join(UPLOAD_DIR, "good_conduct_certificate_barcodes", str(cert.id))
    os.makedirs(barcode_dir, exist_ok=True)
    barcode_path = os.path.join(barcode_dir, "barcode.png")
    from barcode import Code39
    from barcode.writer import ImageWriter
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

@router.get("/good-conduct/{id}", response_model=GoodConductCertificateRead)
def get_good_conduct_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(GoodConductCertificate).filter(GoodConductCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Good Conduct certificate not found")
    cert_data = GoodConductCertificateRead.from_orm(cert)
    image_url_val = getattr(cert, 'image_url', None)
    if image_url_val:
        if str(image_url_val).startswith("http"):
            cert_data.image_url = image_url_val
        else:
            cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
    else:
        cert_data.image_url = None
    barcode_val = getattr(cert, 'barcode', None)
    if barcode_val:
        if str(barcode_val).startswith("http"):
            cert_data.barcode = barcode_val
        else:
            cert_data.barcode = str(request.base_url)[:-1] + f"/{barcode_val}"
    else:
        cert_data.barcode = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data 