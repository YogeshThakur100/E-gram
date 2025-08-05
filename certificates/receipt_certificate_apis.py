from fastapi import APIRouter, Depends, status, Form, HTTPException, Request, Query
from fastapi.responses import FileResponse
import os
import shutil
from sqlalchemy.orm import Session
from database import get_db
from .receipt_certificate_model import ReceiptCertificate
from .receipt_certificate_schemas import ReceiptCertificateCreate, ReceiptCertificateRead
from datetime import datetime
from barcode import Code39
from barcode.writer import ImageWriter
from location_management.models import District, Taluka, GramPanchayat
import location_management.models as location_models

router = APIRouter(prefix="/certificates", tags=["certificates"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/receipt", response_model=ReceiptCertificateRead, status_code=status.HTTP_201_CREATED)
def create_receipt_certificate(
    receipt_date: str = Form(...),
    receipt_id: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    name1: str = Form(None),
    name1_en: str = Form(None),
    name2: str = Form(None),
    name2_en: str = Form(None),
    receipt_amount: str = Form(None),
    receipt_amount_en: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    db: Session = Depends(get_db)
):
    date_obj = datetime.strptime(receipt_date, "%Y-%m-%d").date()
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    cert = ReceiptCertificate(
        receipt_date=date_obj,
        receipt_id=receipt_id,
        village=village,
        village_en=village_en,
        name1=name1,
        name1_en=name1_en,
        name2=name2,
        name2_en=name2_en,
        receipt_amount=receipt_amount,
        receipt_amount_en=receipt_amount_en,
        district_id=district_id_int,
        taluka_id=taluka_id_int,
        gram_panchayat_id=gram_panchayat_id_int
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    # Generate and save barcode image in location-based folder structure
    if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        barcode_dir = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "receipt_certificates", "barcodes", str(cert.id))
    else:
        barcode_dir = os.path.join(UPLOAD_DIR, "receipt_certificates", str(cert.id))
    
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

@router.get("/receipt", response_model=list[ReceiptCertificateRead])
def list_receipt_certificates(
    district_id: int = Query(None, description="Filter by district ID"),
    taluka_id: int = Query(None, description="Filter by taluka ID"),
    gram_panchayat_id: int = Query(None, description="Filter by gram panchayat ID"),
    db: Session = Depends(get_db)
):
    # Validate location hierarchy if any of the three fields are provided
    if district_id is not None:
        district = db.query(location_models.District).filter(location_models.District.id == district_id).first()
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
    
    if taluka_id is not None:
        if district_id is None:
            raise HTTPException(status_code=400, detail="District ID is required when Taluka ID is provided")
        taluka = db.query(location_models.Taluka).filter(
            location_models.Taluka.id == taluka_id,
            location_models.Taluka.district_id == district_id
        ).first()
        if not taluka:
            raise HTTPException(status_code=400, detail="Taluka does not belong to the specified district")
    
    if gram_panchayat_id is not None:
        if taluka_id is None:
            raise HTTPException(status_code=400, detail="Taluka ID is required when Gram Panchayat ID is provided")
        gram_panchayat = db.query(location_models.GramPanchayat).filter(
            location_models.GramPanchayat.id == gram_panchayat_id,
            location_models.GramPanchayat.taluka_id == taluka_id
        ).first()
        if not gram_panchayat:
            raise HTTPException(status_code=400, detail="Gram Panchayat does not belong to the specified taluka")
    
    query = db.query(ReceiptCertificate)
    if district_id:
        query = query.filter(ReceiptCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(ReceiptCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(ReceiptCertificate.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get("/receipt/{id}", response_model=ReceiptCertificateRead)
def get_receipt_certificate(
    id: int, 
    district_id: int = Query(None, description="Filter by district ID"),
    taluka_id: int = Query(None, description="Filter by taluka ID"),
    gram_panchayat_id: int = Query(None, description="Filter by gram panchayat ID"),
    db: Session = Depends(get_db), 
    request: Request = None
):
    # Validate location hierarchy if any of the three fields are provided
    if district_id is not None:
        district = db.query(location_models.District).filter(location_models.District.id == district_id).first()
        if not district:
            raise HTTPException(status_code=404, detail="District not found")
    
    if taluka_id is not None:
        if district_id is None:
            raise HTTPException(status_code=400, detail="District ID is required when Taluka ID is provided")
        taluka = db.query(location_models.Taluka).filter(
            location_models.Taluka.id == taluka_id,
            location_models.Taluka.district_id == district_id
        ).first()
        if not taluka:
            raise HTTPException(status_code=400, detail="Taluka does not belong to the specified district")
    
    if gram_panchayat_id is not None:
        if taluka_id is None:
            raise HTTPException(status_code=400, detail="Taluka ID is required when Gram Panchayat ID is provided")
        gram_panchayat = db.query(location_models.GramPanchayat).filter(
            location_models.GramPanchayat.id == gram_panchayat_id,
            location_models.GramPanchayat.taluka_id == taluka_id
        ).first()
        if not gram_panchayat:
            raise HTTPException(status_code=400, detail="Gram Panchayat does not belong to the specified taluka")
    
    query = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id)
    if district_id:
        query = query.filter(ReceiptCertificate.district_id == district_id)
    if taluka_id:
        query = query.filter(ReceiptCertificate.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(ReceiptCertificate.gram_panchayat_id == gram_panchayat_id)
    
    cert = query.first()
    if not cert:
        raise HTTPException(status_code=404, detail="Receipt certificate not found")
    
    # Populate location names
    if cert.district_id:
        district = db.query(District).filter(District.id == cert.district_id).first()
        cert.gramPanchayat = district.name if district else None
    if cert.taluka_id:
        taluka = db.query(Taluka).filter(Taluka.id == cert.taluka_id).first()
        cert.taluka = taluka.name if taluka else None
    if cert.gram_panchayat_id:
        gram_panchayat = db.query(GramPanchayat).filter(GramPanchayat.id == cert.gram_panchayat_id).first()
        cert.jilha = gram_panchayat.name if gram_panchayat else None
    
    cert_data = ReceiptCertificateRead.from_orm(cert)
    
    # Construct URLs with location query parameters if available
    barcode_val = str(getattr(cert, 'barcode', ''))
    if barcode_val:
        if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/receipt_barcode/{cert.id}?district_id={cert.district_id}&taluka_id={cert.taluka_id}&gram_panchayat_id={cert.gram_panchayat_id}"
        else:
            cert_data.barcode_url = str(request.base_url)[:-1] + f"/certificates/receipt_barcode/{cert.id}"
    else:
        cert_data.barcode_url = None
    
    return cert_data

@router.put("/receipt/{id}", response_model=ReceiptCertificateRead)
def update_receipt_certificate(id: int, receipt_date: str = Form(...),
    receipt_id: str = Form(...),
    village: str = Form(None),
    village_en: str = Form(None),
    name1: str = Form(None),
    name1_en: str = Form(None),
    name2: str = Form(None),
    name2_en: str = Form(None),
    receipt_amount: str = Form(None),
    receipt_amount_en: str = Form(None),
    district_id: str = Form(None),
    taluka_id: str = Form(None),
    gram_panchayat_id: str = Form(None),
    db: Session = Depends(get_db)):
    cert = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Receipt certificate not found")
    
    # Convert location fields to integers
    district_id_int = int(district_id) if district_id and district_id.strip() else None
    taluka_id_int = int(taluka_id) if taluka_id and taluka_id.strip() else None
    gram_panchayat_id_int = int(gram_panchayat_id) if gram_panchayat_id and gram_panchayat_id.strip() else None
    
    date_obj = datetime.strptime(receipt_date, "%Y-%m-%d").date()
    setattr(cert, "receipt_date", date_obj)
    setattr(cert, "receipt_id", receipt_id)
    setattr(cert, "village", village)
    setattr(cert, "village_en", village_en)
    setattr(cert, "name1", name1)
    setattr(cert, "name1_en", name1_en)
    setattr(cert, "name2", name2)
    setattr(cert, "name2_en", name2_en)
    setattr(cert, "receipt_amount", receipt_amount)
    setattr(cert, "receipt_amount_en", receipt_amount_en)
    setattr(cert, "district_id", district_id_int)
    setattr(cert, "taluka_id", taluka_id_int)
    setattr(cert, "gram_panchayat_id", gram_panchayat_id_int)
    # Regenerate barcode in location-based folder structure
    if cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        barcode_dir = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "receipt_certificates", "barcodes", str(cert.id))
    else:
        barcode_dir = os.path.join(UPLOAD_DIR, "receipt_certificates", str(cert.id))
    
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

@router.get("/receipt_barcode/{id}")
def get_receipt_certificate_barcode(
    id: int, 
    district_id: int = Query(None),
    taluka_id: int = Query(None),
    gram_panchayat_id: int = Query(None),
    db: Session = Depends(get_db)
):
    cert = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Receipt certificate not found")
    
    # Determine the barcode path based on location parameters or certificate's stored location
    if district_id and taluka_id and gram_panchayat_id:
        # Validate that provided location matches certificate's location
        if cert.district_id != district_id or cert.taluka_id != taluka_id or cert.gram_panchayat_id != gram_panchayat_id:
            raise HTTPException(status_code=400, detail="Location parameters do not match certificate location")
        barcode_path = os.path.join(UPLOAD_DIR, str(district_id), str(taluka_id), str(gram_panchayat_id), "receipt_certificates", "barcodes", str(id), "barcode.png")
    elif cert.district_id and cert.taluka_id and cert.gram_panchayat_id:
        # Use certificate's stored location
        barcode_path = os.path.join(UPLOAD_DIR, str(cert.district_id), str(cert.taluka_id), str(cert.gram_panchayat_id), "receipt_certificates", "barcodes", str(id), "barcode.png")
    else:
        # Fallback to old path
        barcode_path = os.path.join(UPLOAD_DIR, "receipt_certificates", str(id), "barcode.png")
    
    # Check if file exists in new location, if not try to migrate from old location
    if not os.path.exists(barcode_path):
        old_barcode_path = os.path.join(UPLOAD_DIR, "receipt_certificates", str(id), "barcode.png")
        if os.path.exists(old_barcode_path):
            # Migrate file to new location
            new_dir = os.path.dirname(barcode_path)
            os.makedirs(new_dir, exist_ok=True)
            shutil.copy2(old_barcode_path, barcode_path)
        else:
            raise HTTPException(status_code=404, detail="Barcode file not found")
    
    return FileResponse(barcode_path, media_type="image/png")

@router.put("/receipt/{id}/fix-location")
def fix_receipt_certificate_location(
    id: int,
    district_id: int = Form(...),
    taluka_id: int = Form(...),
    gram_panchayat_id: int = Form(...),
    db: Session = Depends(get_db)
):
    cert = db.query(ReceiptCertificate).filter(ReceiptCertificate.id == id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Receipt certificate not found")
    
    # Update location IDs
    cert.district_id = district_id
    cert.taluka_id = taluka_id
    cert.gram_panchayat_id = gram_panchayat_id
    
    # Migrate barcode file to new location
    old_barcode_path = os.path.join(UPLOAD_DIR, "receipt_certificates", str(id), "barcode.png")
    if os.path.exists(old_barcode_path):
        new_barcode_dir = os.path.join(UPLOAD_DIR, str(district_id), str(taluka_id), str(gram_panchayat_id), "receipt_certificates", "barcodes", str(id))
        new_barcode_path = os.path.join(new_barcode_dir, "barcode.png")
        os.makedirs(new_barcode_dir, exist_ok=True)
        shutil.copy2(old_barcode_path, new_barcode_path)
        # Update the barcode path in database
        cert.barcode = new_barcode_path.replace(os.sep, "/")
    
    db.commit()
    db.refresh(cert)
    
    return {"message": "Location updated and files migrated successfully"}

@router.get("/receipt-all")
def list_all_receipt_certificates(db: Session = Depends(get_db)):
    """Get all Receipt certificates without filters for debugging"""
    certificates = db.query(ReceiptCertificate).all()
    
    # Populate location names for each certificate
    for cert in certificates:
        if cert.district_id:
            district = db.query(District).filter(District.id == cert.district_id).first()
            cert.gramPanchayat = district.name if district else None
        if cert.taluka_id:
            taluka = db.query(Taluka).filter(Taluka.id == cert.taluka_id).first()
            cert.taluka = taluka.name if taluka else None
        if cert.gram_panchayat_id:
            gram_panchayat = db.query(GramPanchayat).filter(GramPanchayat.id == cert.gram_panchayat_id).first()
            cert.jilha = gram_panchayat.name if gram_panchayat else None
    
    return certificates

@router.get("/receipt-debug")
def debug_receipt_certificates(db: Session = Depends(get_db)):
    """Debug endpoint to check receipt certificate data"""
    certificates = db.query(ReceiptCertificate).all()
    
    result = []
    for cert in certificates:
        # Get location names
        district_name = None
        taluka_name = None
        gram_panchayat_name = None
        
        if cert.district_id:
            district = db.query(District).filter(District.id == cert.district_id).first()
            district_name = district.name if district else None
        
        if cert.taluka_id:
            taluka = db.query(Taluka).filter(Taluka.id == cert.taluka_id).first()
            taluka_name = taluka.name if taluka else None
        
        if cert.gram_panchayat_id:
            gram_panchayat = db.query(GramPanchayat).filter(GramPanchayat.id == cert.gram_panchayat_id).first()
            gram_panchayat_name = gram_panchayat.name if gram_panchayat else None
        
        result.append({
            "id": cert.id,
            "receipt_id": cert.receipt_id,
            "village": cert.village,
            "name1": cert.name1,
            "receipt_amount": cert.receipt_amount,
            "district_id": cert.district_id,
            "district_name": district_name,
            "taluka_id": cert.taluka_id,
            "taluka_name": taluka_name,
            "gram_panchayat_id": cert.gram_panchayat_id,
            "gram_panchayat_name": gram_panchayat_name,
            "receipt_date": str(cert.receipt_date) if cert.receipt_date else None
        })
    
    return {
        "total_certificates": len(certificates),
        "certificates": result
    } 