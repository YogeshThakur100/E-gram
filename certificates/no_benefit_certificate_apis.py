from fastapi import APIRouter, Depends, status, Form, UploadFile, File, HTTPException, Request, Query
from typing import List
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
    
    # Debug: Print received values
    
    
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
        # Ensure location fields are not None before creating directory
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            image_dir = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "no_benefit_certificates", "profiles", str(cert.id))
        else:
            # Fallback to old structure if location fields are missing
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
    if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        barcode_dir = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "no_benefit_certificates", "barcodes", str(cert.id))
    else:
        # Fallback to old structure if location fields are missing
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

@router.get("/no-benefit", response_model=List[NoBenefitCertificateRead])
def list_no_benefit_certificates(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    request: Request = None,
    db: Session = Depends(get_db)
):
    query = db.query(NoBenefitCertificate)
    
    # Debug: Print all certificates to see what's stored
    all_certs = db.query(NoBenefitCertificate).all()

    # for cert in all_certs:
        # print(f"DEBUG: Certificate ID {cert.id} - district_id: {cert.district_id}, taluka_id: {cert.taluka_id}, gram_panchayat_id: {cert.gram_panchayat_id}")
    
    if district_id:
        query = query.filter(NoBenefitCertificate.district_id == district_id)
        print(f"DEBUG: Filtering by district_id: {district_id}")
    if taluka_id:
        query = query.filter(NoBenefitCertificate.taluka_id == taluka_id)
        print(f"DEBUG: Filtering by taluka_id: {taluka_id}")
    if gram_panchayat_id:
        query = query.filter(NoBenefitCertificate.gram_panchayat_id == gram_panchayat_id)
        print(f"DEBUG: Filtering by gram_panchayat_id: {gram_panchayat_id}")
    
    certs = query.all()
    result = []
    for cert in certs:
        cert_data = NoBenefitCertificateRead.from_orm(cert)
        # Add barcode_url - only include location parameters if all location fields are present
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
        else:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}"
        
        # Add image_url
        image_url_val = getattr(cert, 'image_url', None)
        if image_url_val and isinstance(image_url_val, str):
            if image_url_val.startswith("http"):
                cert_data.image_url = image_url_val
            else:
                if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
                    cert_data.image_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_image/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
                else:
                    cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
        else:
            cert_data.image_url = None
        
        # Fetch location data
        from location_management import models as location_models
        if cert.district_id:
            district = db.query(location_models.District).filter(location_models.District.id == cert.district_id).first()
            cert_data.jilha = district.name if district else None
        else:
            cert_data.jilha = None
            
        if cert.taluka_id:
            taluka = db.query(location_models.Taluka).filter(location_models.Taluka.id == cert.taluka_id).first()
            cert_data.taluka = taluka.name if taluka else None
        else:
            cert_data.taluka = None
            
        if cert.gram_panchayat_id:
            gram_panchayat = db.query(location_models.GramPanchayat).filter(location_models.GramPanchayat.id == cert.gram_panchayat_id).first()
            cert_data.gramPanchayat = gram_panchayat.name if gram_panchayat else None
        else:
            cert_data.gramPanchayat = None
            
        result.append(cert_data)
    return result

@router.get("/no-benefit-all", response_model=List[NoBenefitCertificateRead])
def list_all_no_benefit_certificates(
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Get all No Benefit certificates without any location filters for debugging"""
    certs = db.query(NoBenefitCertificate).all()
    result = []
    for cert in certs:
        cert_data = NoBenefitCertificateRead.from_orm(cert)
        # Add barcode_url - only include location parameters if all location fields are present
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
        else:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}"
        
        # Add image_url
        image_url_val = getattr(cert, 'image_url', None)
        if image_url_val and isinstance(image_url_val, str):
            if image_url_val.startswith("http"):
                cert_data.image_url = image_url_val
            else:
                if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
                    cert_data.image_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_image/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
                else:
                    cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
        else:
            cert_data.image_url = None
        
        # Fetch location data
        from location_management import models as location_models
        if cert.district_id:
            district = db.query(location_models.District).filter(location_models.District.id == cert.district_id).first()
            cert_data.jilha = district.name if district else None
        else:
            cert_data.jilha = None
            
        if cert.taluka_id:
            taluka = db.query(location_models.Taluka).filter(location_models.Taluka.id == cert.taluka_id).first()
            cert_data.taluka = taluka.name if taluka else None
        else:
            cert_data.taluka = None
            
        if cert.gram_panchayat_id:
            gram_panchayat = db.query(location_models.GramPanchayat).filter(location_models.GramPanchayat.id == cert.gram_panchayat_id).first()
            cert_data.gramPanchayat = gram_panchayat.name if gram_panchayat else None
        else:
            cert_data.gramPanchayat = None
            
        result.append(cert_data)
    return result

@router.get("/no-benefit/{id}", response_model=NoBenefitCertificateRead)
def get_no_benefit_certificate(id: int, request: Request, db: Session = Depends(get_db)):
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="No Benefit certificate not found")
    cert_data = NoBenefitCertificateRead.from_orm(cert)
    # Add barcode_url - only include location parameters if all location fields are present
    if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
    else:
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}"
    
    # Add image_url as absolute URL if present
    image_url_val = getattr(cert, 'image_url', None)
    if image_url_val and isinstance(image_url_val, str):
        if image_url_val.startswith("http"):
            cert_data.image_url = image_url_val
        else:
            if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
                cert_data.image_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_image/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
            else:
                cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
    else:
        cert_data.image_url = None
    
    # Fetch location data
    from location_management import models as location_models
    if cert.district_id:
        district = db.query(location_models.District).filter(location_models.District.id == cert.district_id).first()
        cert_data.jilha = district.name if district else None
    else:
        cert_data.jilha = None
        
    if cert.taluka_id:
        taluka = db.query(location_models.Taluka).filter(location_models.Taluka.id == cert.taluka_id).first()
        cert_data.taluka = taluka.name if taluka else None
    else:
        cert_data.taluka = None
        
    if cert.gram_panchayat_id:
        gram_panchayat = db.query(location_models.GramPanchayat).filter(location_models.GramPanchayat.id == cert.gram_panchayat_id).first()
        cert_data.gramPanchayat = gram_panchayat.name if gram_panchayat else None
    else:
        cert_data.gramPanchayat = None
        
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
        # Ensure location fields are not None before creating directory
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            image_dir = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "no_benefit_certificates", "profiles", str(cert.id))
        else:
            # Fallback to old structure if location fields are missing
            image_dir = os.path.join(UPLOAD_DIR, "nobenefit", "profiles", str(cert.id))
        os.makedirs(image_dir, exist_ok=True)
        file_path = os.path.join(image_dir, safe_filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        setattr(cert, "image_url", file_path.replace(os.sep, "/"))
    db.commit()
    db.refresh(cert)
    # Regenerate barcode
    if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        barcode_dir = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "no_benefit_certificates", "barcodes", str(cert.id))
    else:
        # Fallback to old structure if location fields are missing
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
    # Only construct URLs with location parameters if all location fields are present
    if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
        image_url_val = getattr(cert, 'image_url', None)
        if image_url_val and isinstance(image_url_val, str):
            if image_url_val.startswith("http"):
                cert_data.image_url = image_url_val
            else:
                cert_data.image_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_image/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
        else:
            cert_data.image_url = None
    else:
        # Fallback URLs without location parameters for certificates without location data
        cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/no_benefit_barcode/{cert.id}"
        image_url_val = getattr(cert, 'image_url', None)
        if image_url_val and isinstance(image_url_val, str):
            if image_url_val.startswith("http"):
                cert_data.image_url = image_url_val
            else:
                cert_data.image_url = str(request.base_url)[:-1] + f"/{image_url_val}"
        else:
            cert_data.image_url = None
    
    # Fetch location data
    from location_management import models as location_models
    if cert.district_id:
        district = db.query(location_models.District).filter(location_models.District.id == cert.district_id).first()
        cert_data.jilha = district.name if district else None
    else:
        cert_data.jilha = None
        
    if cert.taluka_id:
        taluka = db.query(location_models.Taluka).filter(location_models.Taluka.id == cert.taluka_id).first()
        cert_data.taluka = taluka.name if taluka else None
    else:
        cert_data.taluka = None
        
    if cert.gram_panchayat_id:
        gram_panchayat = db.query(location_models.GramPanchayat).filter(location_models.GramPanchayat.id == cert.gram_panchayat_id).first()
        cert_data.gramPanchayat = gram_panchayat.name if gram_panchayat else None
    else:
        cert_data.gramPanchayat = None
        
    return cert_data

@router.get("/no_benefit_barcode/{id}")
def get_no_benefit_certificate_barcode(
    id: int,
    district_id: int = Query(None, description="District ID"),
    taluka_id: int = Query(None, description="Taluka ID"),
    gram_panchayat_id: int = Query(None, description="Gram Panchayat ID"),
    db: Session = Depends(get_db)
):
    # Get the certificate first
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="No Benefit certificate not found")
    
    # If location parameters are provided, validate them
    if district_id is not None and taluka_id is not None and gram_panchayat_id is not None:
        from location_management import models as location_models
        district = db.query(location_models.District).filter(location_models.District.id == district_id).first()
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
        
        taluka = db.query(location_models.Taluka).filter(
            location_models.Taluka.id == taluka_id,
            location_models.Taluka.district_id == district_id
        ).first()
        if not taluka:
            raise HTTPException(status_code=400, detail="Taluka does not belong to the specified district")
        
        gram_panchayat = db.query(location_models.GramPanchayat).filter(
            location_models.GramPanchayat.id == gram_panchayat_id,
            location_models.GramPanchayat.taluka_id == taluka_id
        ).first()
        if not gram_panchayat:
            raise HTTPException(status_code=400, detail="Gram Panchayat does not belong to the specified taluka")
        
        # Validate that the certificate belongs to the specified location hierarchy
        if cert.district_id != district_id or cert.taluka_id != taluka_id or cert.gram_panchayat_id != gram_panchayat_id:
            raise HTTPException(status_code=404, detail="No Benefit certificate not found in the specified location")
        
        # Use location-based barcode path
        barcode_path = os.path.join("uploaded_images", str(district_id), str(taluka_id), str(gram_panchayat_id), "no_benefit_certificates", "barcodes", str(id), "barcode.png")
        
        # If file doesn't exist in new location, check old location and migrate
        if not os.path.exists(barcode_path):
            old_barcode_path = os.path.join("uploaded_images", "nobenefit", "barcodes", str(id), "barcode.png")
            if os.path.exists(old_barcode_path):
                # Create new directory structure
                os.makedirs(os.path.dirname(barcode_path), exist_ok=True)
                # Copy file from old location to new location
                import shutil
                shutil.copy2(old_barcode_path, barcode_path)
            else:
                raise HTTPException(status_code=404, detail="Barcode not found")
    else:
        # Use certificate's own location data or fallback to old structure
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            barcode_path = os.path.join("uploaded_images", str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "no_benefit_certificates", "barcodes", str(id), "barcode.png")
        else:
            barcode_path = os.path.join("uploaded_images", "nobenefit", "barcodes", str(id), "barcode.png")
        
        if not os.path.exists(barcode_path):
            raise HTTPException(status_code=404, detail="Barcode not found")
    
    return FileResponse(barcode_path, media_type="image/png")

@router.put("/no-benefit-fix-location/{id}")
def fix_no_benefit_certificate_location(
    id: int,
    district_id: int = Query(..., description="District ID"),
    taluka_id: int = Query(..., description="Taluka ID"),
    gram_panchayat_id: int = Query(..., description="Gram Panchayat ID"),
    db: Session = Depends(get_db)
):
    """Fix location data for existing No Benefit certificates"""
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="No Benefit certificate not found")
    
    # Update location fields
    cert.district_id = district_id
    cert.taluka_id = taluka_id
    cert.gram_panchayat_id = gram_panchayat_id
    
    # Move files to correct location if they exist
    old_barcode_path = os.path.join("uploaded_images", "nobenefit", "barcodes", str(id), "barcode.png")
    new_barcode_path = os.path.join("uploaded_images", str(district_id), str(taluka_id), str(gram_panchayat_id), "no_benefit_certificates", "barcodes", str(id), "barcode.png")
    
    if os.path.exists(old_barcode_path):
        os.makedirs(os.path.dirname(new_barcode_path), exist_ok=True)
        import shutil
        shutil.copy2(old_barcode_path, new_barcode_path)
        cert.barcode = new_barcode_path.replace(os.sep, "/")
    
    old_image_path = os.path.join("uploaded_images", "nobenefit", "profiles", str(id))
    new_image_path = os.path.join("uploaded_images", str(district_id), str(taluka_id), str(gram_panchayat_id), "no_benefit_certificates", "profiles", str(id))
    
    if os.path.exists(old_image_path):
        os.makedirs(new_image_path, exist_ok=True)
        import shutil
        for file in os.listdir(old_image_path):
            old_file = os.path.join(old_image_path, file)
            new_file = os.path.join(new_image_path, file)
            shutil.copy2(old_file, new_file)
        cert.image_url = new_image_path.replace(os.sep, "/")
    
    db.commit()
    db.refresh(cert)
    
    return {"message": f"Certificate {id} location updated successfully", "certificate": cert}

@router.get("/no_benefit_image/{id}")
def get_no_benefit_certificate_image(
    id: int,
    district_id: int = Query(None, description="District ID"),
    taluka_id: int = Query(None, description="Taluka ID"),
    gram_panchayat_id: int = Query(None, description="Gram Panchayat ID"),
    db: Session = Depends(get_db)
):
    # Get the certificate first
    cert = db.query(NoBenefitCertificate).filter(NoBenefitCertificate.id == id).first()
    if not cert or not getattr(cert, "image_url", None):
        raise HTTPException(status_code=404, detail="No Benefit certificate image not found")
    
    # If location parameters are provided, validate them
    if district_id is not None and taluka_id is not None and gram_panchayat_id is not None:
        from location_management import models as location_models
        district = db.query(location_models.District).filter(location_models.District.id == district_id).first()
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
        
        taluka = db.query(location_models.Taluka).filter(
            location_models.Taluka.id == taluka_id,
            location_models.Taluka.district_id == district_id
        ).first()
        if not taluka:
            raise HTTPException(status_code=400, detail="Taluka does not belong to the specified district")
        
        gram_panchayat = db.query(location_models.GramPanchayat).filter(
            location_models.GramPanchayat.id == gram_panchayat_id,
            location_models.GramPanchayat.taluka_id == taluka_id
        ).first()
        if not gram_panchayat:
            raise HTTPException(status_code=400, detail="Gram Panchayat does not belong to the specified taluka")
        
        # Validate that the certificate belongs to the specified location hierarchy
        if cert.district_id != district_id or cert.taluka_id != taluka_id or cert.gram_panchayat_id != gram_panchayat_id:
            raise HTTPException(status_code=404, detail="No Benefit certificate image not found in the specified location")
        
        # Use location-based image path
        image_path = os.path.join("uploaded_images", str(district_id), str(taluka_id), str(gram_panchayat_id), "no_benefit_certificates", "profiles", str(id))
        
        # If file doesn't exist in new location, check old location and migrate
        if not os.path.exists(image_path):
            old_image_path = os.path.join("uploaded_images", "nobenefit", "profiles", str(id))
            if os.path.exists(old_image_path):
                # Create new directory structure
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                # Copy files from old location to new location
                import shutil
                for file in os.listdir(old_image_path):
                    old_file = os.path.join(old_image_path, file)
                    new_file = os.path.join(image_path, file)
                    shutil.copy2(old_file, new_file)
            else:
                raise HTTPException(status_code=404, detail="Image not found")
    else:
        # Use certificate's own location data or fallback to old structure
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            image_path = os.path.join("uploaded_images", str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "no_benefit_certificates", "profiles", str(id))
        else:
            image_path = os.path.join("uploaded_images", "nobenefit", "profiles", str(id))
        
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")
    
    # Find the image file in the directory
    if os.path.exists(image_path) and os.path.isdir(image_path):
        for file in os.listdir(image_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                return FileResponse(os.path.join(image_path, file), media_type="image/png")
    
    raise HTTPException(status_code=404, detail="Image file not found") 