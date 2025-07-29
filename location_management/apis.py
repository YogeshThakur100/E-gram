from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import models, schemas

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
def get_gram_panchayat(gram_panchayat_id: int, db: Session = Depends(get_db)):
    """Get a specific gram panchayat by ID"""
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat:
        raise HTTPException(status_code=404, detail="Gram Panchayat not found")
    return gram_panchayat

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
    
    db.delete(db_gram_panchayat)
    db.commit()
    return {"message": "Gram Panchayat deleted successfully"} 