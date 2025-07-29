# Helper functions for location management database operations
from sqlalchemy.orm import Session
from typing import List, Optional
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