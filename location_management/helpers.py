# Helper functions for location management database operations
import os
import shutil
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import UploadFile
from . import models, schemas


def get_district_by_name(db: Session, name: str) -> Optional[models.District]:
    """Get district by name"""
    return db.query(models.District).filter(models.District.name == name).first()


def get_taluka_by_name_and_district(db: Session, name: str, district_id: int) -> Optional[models.Taluka]:
    """Get taluka by name and district"""
    return db.query(models.Taluka).filter(
        models.Taluka.name == name,
        models.Taluka.district_id == district_id
    ).first()


def get_gram_panchayat_by_name_and_taluka(db: Session, name: str, taluka_id: int) -> Optional[models.GramPanchayat]:
    """Get gram panchayat by name and taluka"""
    return db.query(models.GramPanchayat).filter(
        models.GramPanchayat.name == name,
        models.GramPanchayat.taluka_id == taluka_id
    ).first()


def get_districts_with_talukas(db: Session) -> List[models.District]:
    """Get all districts with their talukas"""
    return db.query(models.District).options(
        db.joinedload(models.District.talukas)
    ).all()


def get_talukas_with_gram_panchayats(db: Session) -> List[models.Taluka]:
    """Get all talukas with their gram panchayats"""
    return db.query(models.Taluka).options(
        db.joinedload(models.Taluka.gram_panchayats)
    ).all()


def get_location_hierarchy(db: Session) -> List[dict]:
    """Get complete location hierarchy for frontend"""
    districts = get_districts_with_talukas(db)
    result = []
    
    for district in districts:
        district_data = {
            "id": district.id,
            "name": district.name,
            "code": district.code,
            "talukas": []
        }
        
        for taluka in district.talukas:
            taluka_data = {
                "id": taluka.id,
                "name": taluka.name,
                "code": taluka.code,
                "district_id": taluka.district_id,
                "gram_panchayats": []
            }
            
            # Get gram panchayats for this taluka
            gram_panchayats = db.query(models.GramPanchayat).filter(
                models.GramPanchayat.taluka_id == taluka.id
            ).all()
            
            for gram_panchayat in gram_panchayats:
                taluka_data["gram_panchayats"].append({
                    "id": gram_panchayat.id,
                    "name": gram_panchayat.name,
                    "code": gram_panchayat.code,
                    "taluka_id": gram_panchayat.taluka_id
                })
            
            district_data["talukas"].append(taluka_data)
        
        result.append(district_data)
    
    return result


# Image upload helper functions
UPLOAD_DIR = "uploaded_images"

def save_gram_panchayat_image(db: Session, gram_panchayat_id: int, image: UploadFile) -> str:
    """Save gram panchayat image and return the file path"""
    # Get gram panchayat to find district and taluka IDs
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat:
        raise ValueError("Gram panchayat not found")
    
    # Get taluka to find district ID
    taluka = db.query(models.Taluka).filter(models.Taluka.id == gram_panchayat.taluka_id).first()
    if not taluka:
        raise ValueError("Taluka not found")
    
    # Create directory structure: uploaded_images/{district_id}/{taluka_id}/{gram_panchayat_id}/
    image_dir = os.path.join(UPLOAD_DIR, str(taluka.district_id), str(taluka.id), str(gram_panchayat_id))
    os.makedirs(image_dir, exist_ok=True)
    
    # Create safe filename (replace spaces with underscores)
    safe_filename = image.filename.replace(' ', '_')
    file_path = os.path.join(image_dir, safe_filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Return relative path for database storage
    return file_path.replace(os.sep, "/")


def remove_gram_panchayat_image(db: Session, gram_panchayat_id: int) -> bool:
    """Remove gram panchayat image file"""
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat or not gram_panchayat.image_url:
        return False
    
    try:
        # Convert URL path back to file system path
        file_path = gram_panchayat.image_url.replace("/", os.sep)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception:
        pass
    
    return False


def get_gram_panchayat_image_path(db: Session, gram_panchayat_id: int) -> Optional[str]:
    """Get gram panchayat image file path"""
    gram_panchayat = db.query(models.GramPanchayat).filter(models.GramPanchayat.id == gram_panchayat_id).first()
    if not gram_panchayat or not gram_panchayat.image_url:
        return None
    
    return gram_panchayat.image_url.replace("/", os.sep) 