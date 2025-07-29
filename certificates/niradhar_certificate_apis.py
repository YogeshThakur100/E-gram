from fastapi import APIRouter, Depends, status, Form, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .niradhar_certificate_model import NiradharCertificate
from .niradhar_certificate_schemas import NiradharCertificateCreate, NiradharCertificateRead
from datetime import datetime
from barcode import Code39
from barcode.writer import ImageWriter
import os

router = APIRouter(prefix="/certificates", tags=["certificates"])

@router.post("/niradhar", response_model=NiradharCertificateRead, status_code=status.HTTP_201_CREATED)
def create_niradhar_certificate(
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
    db: Session = Depends(get_db)
):
    reg_date_obj = datetime.strptime(registration_date, "%Y-%m-%d").date()
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    cert = NiradharCertificate(
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
    # Generate and save barcode image
    barcode_dir = os.path.join("uploaded_images", "niradhar_certificate_barcodes", str(cert.id))
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
    db.commit()
    db.refresh(cert)
    return cert

@router.get("/niradhar", response_model=list[NiradharCertificateRead])
def list_niradhar_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    query = db.query(NiradharCertificate)
    if district_id:
        query = query.filter(NiradharCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(NiradharCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(NiradharCertificate.gram_panchayat_id == gram_panchayat_id)
    certs = query.all()
    result = []
    for cert in certs:
        cert_data = NiradharCertificateRead.from_orm(cert)
        barcode_val = getattr(cert, 'barcode', None)
        if barcode_val:
            if str(barcode_val).startswith("http"):
                cert_data.barcode_url = barcode_val
            else:
                cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}"
        else:
            cert_data.barcode_url = None
        cert_data.gramPanchayat = None
        cert_data.taluka = None
        cert_data.jilha = None
        result.append(cert_data)
    return result

@router.get("/niradhar/{id}", response_model=NiradharCertificateRead)
def get_niradhar_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(NiradharCertificate).filter(NiradharCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Niradhar certificate not found")
    cert_data = NiradharCertificateRead.from_orm(cert)
    barcode_val = getattr(cert, 'barcode', None)
    if barcode_val:
        if str(barcode_val).startswith("http"):
            cert_data.barcode_url = barcode_val
        else:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}"
    else:
        cert_data.barcode_url = None
    cert_data.gramPanchayat = None
    cert_data.taluka = None
    cert_data.jilha = None
    return cert_data

@router.put("/niradhar/{id}", response_model=NiradharCertificateRead)
def update_niradhar_certificate(
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
    db: Session = Depends(get_db)):
    cert = db.query(NiradharCertificate).filter(NiradharCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Niradhar certificate not found")
    
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
    # Regenerate barcode
    barcode_dir = os.path.join("uploaded_images", "niradhar_certificate_barcodes", str(cert.id))
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
    db.commit()
    db.refresh(cert)
    cert_data = NiradharCertificateRead.from_orm(cert)
    barcode_val = getattr(cert, 'barcode', None)
    if barcode_val:
        if str(barcode_val).startswith("http"):
            cert_data.barcode_url = barcode_val
        else:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/{barcode_val}"
    else:
        cert_data.barcode_url = None
    return cert_data 