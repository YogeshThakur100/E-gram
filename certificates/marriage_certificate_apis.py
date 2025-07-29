from fastapi import APIRouter, Depends, status, Form, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .marriage_certificate_model import MarriageCertificate
from .marriage_certificate_schemas import MarriageCertificateCreate, MarriageCertificateRead
from datetime import datetime
import os
from barcode import Code39
from barcode.writer import ImageWriter
import qrcode

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/marriage", response_model=MarriageCertificateRead, status_code=status.HTTP_201_CREATED)
def create_marriage_certificate(
    id: int = Form(...),
    registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    husband_name: str = Form(None),
    husband_name_en: str = Form(None),
    husband_adhar: str = Form(None),
    husband_adhar_en: str = Form(None),
    husband_address: str = Form(None),
    husband_address_en: str = Form(None),
    wife_name: str = Form(None),
    wife_name_en: str = Form(None),
    wife_adhar: str = Form(None),
    wife_adhar_en: str = Form(None),
    wife_address: str = Form(None),
    wife_address_en: str = Form(None),
    marriage_date: str = Form(...),
    marriage_register_no: str = Form(None),
    marriage_register_subno: str = Form(None),
    marriage_place: str = Form(None),
    marriage_place_en: str = Form(None),
    remark: str = Form(None),
    remark_en: str = Form(None),
    district_id: int = Form(None),
    taluka_id: int = Form(None),
    gram_panchayat_id: int = Form(None),
    db: Session = Depends(get_db)
):
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    marriage_date_obj = datetime.strptime(marriage_date, "%Y-%m-%d").date()
    cert = MarriageCertificate(
        id=id,
        registration_date=reg_date_obj,
        village=village,
        village_en=village_en,
        husband_name=husband_name,
        husband_name_en=husband_name_en,
        husband_adhar=husband_adhar,
        husband_adhar_en=husband_adhar_en,
        husband_address=husband_address,
        husband_address_en=husband_address_en,
        wife_name=wife_name,
        wife_name_en=wife_name_en,
        wife_adhar=wife_adhar,
        wife_adhar_en=wife_adhar_en,
        wife_address=wife_address,
        wife_address_en=wife_address_en,
        marriage_date=marriage_date_obj,
        marriage_register_no=marriage_register_no,
        marriage_register_subno=marriage_register_subno,
        marriage_place=marriage_place,
        marriage_place_en=marriage_place_en,
        remark=remark,
        remark_en=remark_en,
        district_id=district_id,
        taluka_id=taluka_id,
        gram_panchayat_id=gram_panchayat_id
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Generate and save barcode image
    barcode_dir = os.path.join("uploaded_images", "marriage_certificates", "barcode", str(cert.id))
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
    setattr(cert, 'barcode', barcode_path.replace(os.sep, "/"))
    # Generate and save QR code image with required data
    qrcode_dir = os.path.join("uploaded_images", "marriage_certificates", "qrcode", str(cert.id))
    os.makedirs(qrcode_dir, exist_ok=True)
    qrcode_path = os.path.join(qrcode_dir, "qrcode.png")
    qr_data = f"srno: {cert.id}\nreg date: {cert.registration_date}\nmarriage date: {cert.marriage_date}\nhusband name: {cert.husband_name_en or ''}\nwife name: {cert.wife_name_en or ''}\nmarriage place: {cert.marriage_place_en or ''}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    with open(qrcode_path, "wb") as f:
        img.save(f)
    setattr(cert, 'qrcode', qrcode_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/marriage", response_model=list[MarriageCertificateRead])
def list_marriage_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    request: Request = None, 
    db: Session = Depends(get_db)
):
    query = db.query(MarriageCertificate)
    
    # Apply location filters if provided
    if district_id:
        query = query.filter(MarriageCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(MarriageCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(MarriageCertificate.gram_panchayat_id == gram_panchayat_id)
    
    certs = query.all()
    result = []
    for cert in certs:
        cert_data = MarriageCertificateRead.from_orm(cert)
        # Absolute URLs
        barcode_val = str(getattr(cert, 'barcode', ''))
        if barcode_val:
            cert_data.barcode = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
        else:
            cert_data.barcode = None
        qrcode_val = str(getattr(cert, 'qrcode', ''))
        if qrcode_val:
            cert_data.qrcode = str(request.base_url)[:-1] + f"/{qrcode_val}" if not qrcode_val.startswith("http") else qrcode_val
        else:
            cert_data.qrcode = None
        cert_data.gramPanchayat = None
        cert_data.taluka = None
        cert_data.jilha = None
        result.append(cert_data)
    return result

@router.get("/marriage/{id}", response_model=MarriageCertificateRead)
def get_marriage_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(MarriageCertificate).filter(MarriageCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Marriage certificate not found")
    cert_data = MarriageCertificateRead.from_orm(cert)
    barcode_val = str(getattr(cert, 'barcode', ''))
    if barcode_val:
        cert_data.barcode = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
    else:
        cert_data.barcode = None
    qrcode_val = str(getattr(cert, 'qrcode', ''))
    if qrcode_val:
        cert_data.qrcode = str(request.base_url)[:-1] + f"/{qrcode_val}" if not qrcode_val.startswith("http") else qrcode_val
    else:
        cert_data.qrcode = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/marriage/{id}", response_model=MarriageCertificateRead)
def update_marriage_certificate(
    id: int,
    request: Request,
    registration_date: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    husband_name: str = Form(None),
    husband_name_en: str = Form(None),
    husband_adhar: str = Form(None),
    husband_adhar_en: str = Form(None),
    husband_address: str = Form(None),
    husband_address_en: str = Form(None),
    wife_name: str = Form(None),
    wife_name_en: str = Form(None),
    wife_adhar: str = Form(None),
    wife_adhar_en: str = Form(None),
    wife_address: str = Form(None),
    wife_address_en: str = Form(None),
    marriage_date: str = Form(...),
    marriage_register_no: str = Form(None),
    marriage_register_subno: str = Form(None),
    marriage_place: str = Form(None),
    marriage_place_en: str = Form(None),
    remark: str = Form(None),
    remark_en: str = Form(None),
    district_id: int = Form(None),
    taluka_id: int = Form(None),
    gram_panchayat_id: int = Form(None),
    db: Session = Depends(get_db)):
    cert = db.query(MarriageCertificate).filter(MarriageCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Marriage certificate not found")
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    marriage_date_obj = datetime.strptime(marriage_date, "%Y-%m-%d").date()
    setattr(cert, "registration_date", reg_date_obj)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "husband_name", husband_name)
    setattr(cert, "husband_name_en", husband_name_en)
    setattr(cert, "husband_adhar", husband_adhar)
    setattr(cert, "husband_adhar_en", husband_adhar_en)
    setattr(cert, "husband_address", husband_address)
    setattr(cert, "husband_address_en", husband_address_en)
    setattr(cert, "wife_name", wife_name)
    setattr(cert, "wife_name_en", wife_name_en)
    setattr(cert, "wife_adhar", wife_adhar)
    setattr(cert, "wife_adhar_en", wife_adhar_en)
    setattr(cert, "wife_address", wife_address)
    setattr(cert, "wife_address_en", wife_address_en)
    setattr(cert, "marriage_date", marriage_date_obj)
    setattr(cert, "marriage_register_no", marriage_register_no)
    setattr(cert, "marriage_register_subno", marriage_register_subno)
    setattr(cert, "marriage_place", marriage_place)
    setattr(cert, "marriage_place_en", marriage_place_en)
    setattr(cert, "remark", remark)
    setattr(cert, "remark_en", remark_en)
    setattr(cert, "district_id", district_id)
    setattr(cert, "taluka_id", taluka_id)
    setattr(cert, "gram_panchayat_id", gram_panchayat_id)
    # Regenerate barcode
    barcode_dir = os.path.join("uploaded_images", "marriage_certificates", "barcode", str(cert.id))
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
    setattr(cert, 'barcode', barcode_path.replace(os.sep, "/"))
    # Regenerate QR code
    qrcode_dir = os.path.join("uploaded_images", "marriage_certificates", "qrcode", str(cert.id))
    os.makedirs(qrcode_dir, exist_ok=True)
    qrcode_path = os.path.join(qrcode_dir, "qrcode.png")
    qr_data = f"srno: {cert.id}\nreg date: {cert.registration_date}\nmarriage date: {cert.marriage_date}\nhusband name: {cert.husband_name_en or ''}\nwife name: {cert.wife_name_en or ''}\nmarriage place: {cert.marriage_place_en or ''}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    with open(qrcode_path, "wb") as f:
        img.save(f)
    setattr(cert, 'qrcode', qrcode_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    cert_data = MarriageCertificateRead.from_orm(cert)
    barcode_val = str(getattr(cert, 'barcode', ''))
    if barcode_val:
        cert_data.barcode = str(request.base_url)[:-1] + f"/{barcode_val}" if not barcode_val.startswith("http") else barcode_val
    else:
        cert_data.barcode = None
    qrcode_val = str(getattr(cert, 'qrcode', ''))
    if qrcode_val:
        cert_data.qrcode = str(request.base_url)[:-1] + f"/{qrcode_val}" if not qrcode_val.startswith("http") else qrcode_val
    else:
        cert_data.qrcode = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data 