from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import database
from namuna8 import namuna8_model as models

router = APIRouter(prefix="/madhila", tags=["Madhila APIs"])

@router.get("/property_list_with_owners/", response_model=List[dict])
def get_property_list_with_owners(village: str, db: Session = Depends(database.get_db)):
    village_obj = db.query(models.Village).filter(models.Village.name == village).first()
    if not village_obj:
        return []
    properties = db.query(models.Property).filter(models.Property.village_id == village_obj.id).all()
    result = []
    for p in properties:
        owners_list = []
        if p.owners:
            for o in p.owners:
                owners_list.append({
                    "id": o.id,
                    "name": o.name,
                    "holderno": o.holderno
                })
            owner_name = ','.join([f"{i+1}.{o['name']}" for i, o in enumerate(owners_list)])
        else:
            owner_name = "N/A"
        result.append({
            "malmattaKramank": p.malmattaKramank,
            "ownerName": owner_name,
            "anuKramank": p.anuKramank,
            "owners": owners_list
        })
    return result 