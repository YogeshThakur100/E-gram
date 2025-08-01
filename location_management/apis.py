import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import models, schemas, helpers

router = APIRouter(prefix="/location", tags=["Location Management"])

# ==================== DISTRICT APIs ====================

@router.get("/districts", response_model=List[schemas.DistrictRead])
def get_all_districts(db: Session = Depends(get_db)):
    """Get all districts"""
    districts = db.query(models.District).all()
    return districts

@router.get("/districts/{district_id}", response_model=schemas.DistrictRead)
def get_district(district_id: int, db: Session = Depends(get_db)):
    """Get a specific district by ID"""
    district = db.query(models.District).filter(models.District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@router.post("/districts", response_model=schemas.DistrictRead, status_code=status.HTTP_201_CREATED)
def create_district(district: schemas.DistrictCreate, db: Session = Depends(get_db)):
    """Create a new district"""
    # Check if district with same name already exists
    existing_district = db.query(models.District).filter(models.District.name == district.name).first()
    if existing_district:
        raise HTTPException(status_code=400, detail="District with this name already exists")
    
    db_district = models.District(**district.dict())
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

@router.put("/districts/{district_id}", response_model=schemas.DistrictRead)
def update_district(district_id: int, district: schemas.DistrictUpdate, db: Session = Depends(get_db)):
    """Update a district"""
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if not db_district:
        raise HTTPException(status_code=404, detail="District not found")
    
    update_data = district.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_district, field, value)
    
    db.commit()
    db.refresh(db_district)
    return db_district

@router.delete("/districts/{district_id}")
def delete_district(district_id: int, db: Session = Depends(get_db)):
    """Delete a district"""
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if not db_district:
        raise HTTPException(status_code=404, detail="District not found")
    
    db.delete(db_district)
    db.commit()
    return {"message": "District deleted successfully"}

# ==================== TALUKA APIs ====================

@router.get("/talukas", response_model=List[schemas.TalukaRead])
def get_all_talukas(db: Session = Depends(get_db)):
    """Get all talukas"""
    talukas = db.query(models.Taluka).all()
    return talukas

@router.get("/talukas/district/{district_id}", response_model=List[schemas.TalukaRead])
def get_talukas_by_district(district_id: int, db: Session = Depends(get_db)):
    """Get all talukas for a specific district"""
    talukas = db.query(models.Taluka).filter(models.Taluka.district_id == district_id).all()
    return talukas

@router.get("/talukas/{taluka_id}", response_model=schemas.TalukaRead)
def get_taluka(taluka_id: int, db: Session = Depends(get_db)):
    """Get a specific taluka by ID"""
    taluka = db.query(models.Taluka).filter(models.Taluka.id == taluka_id).first()
    if not taluka:
        raise HTTPException(status_code=404, detail="Taluka not found")
    return taluka

@router.post("/talukas", response_model=schemas.TalukaRead, status_code=status.HTTP_201_CREATED)
def create_taluka(taluka: schemas.TalukaCreate, db: Session = Depends(get_db)):
    """Create a new taluka"""
    # Check if district exists
    district = db.query(models.District).filter(models.District.id == taluka.district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    
    # Check if taluka with same name in same district already exists
    existing_taluka = db.query(models.Taluka).filter(
        models.Taluka.name == taluka.name,
        models.Taluka.district_id == taluka.district_id
    ).first()
    if existing_taluka:
        raise HTTPException(status_code=400, detail="Taluka with this name already exists in this district")
    
    db_taluka = models.Taluka(**taluka.dict())
    db.add(db_taluka)
    db.commit()
    db.refresh(db_taluka)
    return db_taluka

@router.put("/talukas/{taluka_id}", response_model=schemas.TalukaRead)
def update_taluka(taluka_id: int, taluka: schemas.TalukaUpdate, db: Session = Depends(get_db)):
    """Update a taluka"""
    db_taluka = db.query(models.Taluka).filter(models.Taluka.id == taluka_id).first()
    if not db_taluka:
        raise HTTPException(status_code=404, detail="Taluka not found")
    
    update_data = taluka.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_taluka, field, value)
    
    db.commit()
    db.refresh(db_taluka)
    return db_taluka

@router.delete("/talukas/{taluka_id}")
def delete_taluka(taluka_id: int, db: Session = Depends(get_db)):
    """Delete a taluka"""
    db_taluka = db.query(models.Taluka).filter(models.Taluka.id == taluka_id).first()
    if not db_taluka:
        raise HTTPException(status_code=404, detail="Taluka not found")
    
    db.delete(db_taluka)
    db.commit()
    return {"message": "Taluka deleted successfully"}

# ==================== GRAM PANCHAYAT APIs ====================

@router.get("/gram-panchayats", response_model=List[schemas.GramPanchayatRead])
def get_all_gram_panchayats(db: Session = Depends(get_db)):
    """Get all gram panchayats"""
    gram_panchayats = db.query(models.GramPanchayat).all()
    return gram_panchayats

@router.get("/gram-panchayats/taluka/{taluka_id}", response_model=List[schemas.GramPanchayatRead])
def get_gram_panchayats_by_taluka(taluka_id: int, db: Session = Depends(get_db)):
    """Get all gram panchayats for a specific taluka"""
    gram_panchayats = db.query(models.GramPanchayat).filter(models.GramPanchayat.taluka_id == taluka_id).all()
    return gram_panchayats

@router.get("/gram-panchayats/{gram_panchayat_id}", response_model=schemas.GramPanchayatRead)
def get_gram_panchayat(gram_panchayat_id: int, request: Request, db: Session = Depends(get_db)):
    """Get a specific gram panchayat by ID"""
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    
    # Convert to response model
    gram_panchayat_data = schemas.GramPanchayatRead.from_orm(gram_panchayat)
    
    # Add absolute URL for image if present
    if gram_panchayat.image_url:
        if gram_panchayat.image_url.startswith("http"):
            gram_panchayat_data.image_url = gram_panchayat.image_url
        else:
            gram_panchayat_data.image_url = str(request.base_url)[:-1] + f"/{gram_panchayat.image_url}"
    
    return gram_panchayat_data

@router.post("/gram-panchayats", response_model=schemas.GramPanchayatRead, status_code=status.HTTP_201_CREATED)
def create_gram_panchayat(gram_panchayat: schemas.GramPanchayatCreate, db: Session = Depends(get_db)):
    """Create a new gram panchayat"""
    # Check if taluka exists
    taluka = db.query(models.Taluka).filter(models.Taluka.id == gram_panchayat.taluka_id).first()
    if not taluka:
        raise HTTPException(status_code=404, detail="Taluka not found")
    
    # Check if gram panchayat with same name in same taluka already exists
    existing_gram_panchayat = db.query(models.GramPanchayat).filter(
        models.GramPanchayat.name == gram_panchayat.name,
        models.GramPanchayat.taluka_id == gram_panchayat.taluka_id
    ).first()
    if existing_gram_panchayat:
        raise HTTPException(status_code=400, detail="Gram Panchayat with this name already exists in this taluka")
    
    db_gram_panchayat = models.GramPanchayat(**gram_panchayat.dict())
    db.add(db_gram_panchayat)
    db.commit()
    db.refresh(db_gram_panchayat)
    return db_gram_panchayat

@router.put("/gram-panchayats/{gram_panchayat_id}", response_model=schemas.GramPanchayatRead)
def update_gram_panchayat(gram_panchayat_id: int, gram_panchayat: schemas.GramPanchayatUpdate, db: Session = Depends(get_db)):
    """Update a gram panchayat"""
    db_gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not db_gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    
    update_data = gram_panchayat.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_gram_panchayat, field, value)
    
    db.commit()
    db.refresh(db_gram_panchayat)
    return db_gram_panchayat

@router.delete("/gram-panchayats/{gram_panchayat_id}")
def delete_gram_panchayat(gram_panchayat_id: int, db: Session = Depends(get_db)):
    """Delete a gram panchayat"""
    db_gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not db_gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    
    # Remove image file if exists
    if db_gram_panchayat.image_url:
        helpers.remove_gram_panchayat_image(db, gram_panchayat_id)
    
    db.delete(db_gram_panchayat)
    db.commit()
    return {"message": "Gram Panchayat deleted successfully"}


# ==================== GRAM PANCHAYAT IMAGE APIs ====================

@router.post("/gram-panchayats/{gram_panchayat_id}/image", response_model=schemas.GramPanchayatRead)
def upload_gram_panchayat_image(
    gram_panchayat_id: int,
    image: UploadFile = File(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Upload image for a gram panchayat"""
    # Check if gram panchayat exists
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    
    # Validate image file
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Remove existing image if any
        if gram_panchayat.image_url:
            helpers.remove_gram_panchayat_image(db, gram_panchayat_id)
        
        # Save new image
        image_path = helpers.save_gram_panchayat_image(db, gram_panchayat_id, image)
        
        # Update database
        gram_panchayat.image_url = image_path
        db.commit()
        db.refresh(gram_panchayat)
        
        # Convert to response model
        gram_panchayat_data = schemas.GramPanchayatRead.from_orm(gram_panchayat)
        
        # Add absolute URL for image
        if request:
            gram_panchayat_data.image_url = str(request.base_url)[:-1] + f"/{image_path}"
        
        return gram_panchayat_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


@router.put("/gram-panchayats/{gram_panchayat_id}/image", response_model=schemas.GramPanchayatRead)
def update_gram_panchayat_image(
    gram_panchayat_id: int,
    image: UploadFile = File(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Update image for a gram panchayat"""
    # Check if gram panchayat exists
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    
    # Validate image file
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Remove existing image
        if gram_panchayat.image_url:
            helpers.remove_gram_panchayat_image(db, gram_panchayat_id)
        
        # Save new image
        image_path = helpers.save_gram_panchayat_image(db, gram_panchayat_id, image)
        
        # Update database
        gram_panchayat.image_url = image_path
        db.commit()
        db.refresh(gram_panchayat)
        
        # Convert to response model
        gram_panchayat_data = schemas.GramPanchayatRead.from_orm(gram_panchayat)
        
        # Add absolute URL for image
        if request:
            gram_panchayat_data.image_url = str(request.base_url)[:-1] + f"/{image_path}"
        
        return gram_panchayat_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update image: {str(e)}")


@router.delete("/gram-panchayats/{gram_panchayat_id}/image")
def remove_gram_panchayat_image(gram_panchayat_id: int, db: Session = Depends(get_db)):
    """Remove image from a gram panchayat"""
    # Check if gram panchayat exists
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    
    if not gram_panchayat.image_url:
        raise HTTPException(status_code=404, detail="No image found for this gram panchayat")
    
    try:
        # Remove image file
        if helpers.remove_gram_panchayat_image(db, gram_panchayat_id):
            # Update database
            gram_panchayat.image_url = None
            db.commit()
            return {"message": "Image removed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to remove image file")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove image: {str(e)}")


@router.get("/gram-panchayats/{gram_panchayat_id}/image")
def serve_gram_panchayat_image(gram_panchayat_id: int, db: Session = Depends(get_db)):
    """Serve gram panchayat image"""
    from fastapi.responses import FileResponse
    
    # Get image path
    image_path = helpers.get_gram_panchayat_image_path(db, gram_panchayat_id)
    if not image_path or not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path) 