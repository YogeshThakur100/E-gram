from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db
from ..namuna8_model import Owner
from ..namuna8_apis import build_property_response
from .. import namuna8_model

router = APIRouter()

@router.get("/owners_with_properties_by_village/")
def owners_with_properties_by_village(village_id: int, db: Session = Depends(get_db)):
    owners = db.query(namuna8_model.Owner).filter(namuna8_model.Owner.village_id == village_id).all()
    result = []
    for owner in owners:
        owner_dict = {
            "id": owner.id,
            "name": owner.name,
            "aadhaarNumber": owner.aadhaarNumber,
            "mobileNumber": owner.mobileNumber,
            "wifeName": owner.wifeName,
            "occupantName": owner.occupantName,
            "ownerPhoto": owner.ownerPhoto,
            "village_id": owner.village_id,
            "properties": [build_property_response(p, db) for p in owner.properties]
        }
        result.append(owner_dict)
    return result

@router.delete("/owners/delete/")
def delete_owners(owner_ids: list[int] = Body(...), db: Session = Depends(get_db)):
    for owner_id in owner_ids:
        owner = db.query(namuna8_model.Owner).filter(namuna8_model.Owner.id == owner_id).first()
        if not owner:
            continue
        # Remove owner from all properties
        for prop in owner.properties:
            prop.owners = [o for o in prop.owners if o.id != owner_id]
        db.delete(owner)
    db.commit()
    return {"success": True, "deleted_owner_ids": owner_ids} 