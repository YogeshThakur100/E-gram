from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from ..namuna8_model import Owner, Property

from pydantic import BaseModel

router = APIRouter()

class OwnerTransferRequest(BaseModel):
    from_village_id: int
    to_village_id: int
    owner_ids: List[int]
    district_id: int = None
    taluka_id: int = None
    gram_panchayat_id: int = None

# @router.post("/owners/transfer/")
# def transfer_owners(request: OwnerTransferRequest, db: Session = Depends(get_db)):
#     owners = db.query(Owner).filter(Owner.id.in_(request.owner_ids), Owner.village_id == request.from_village_id).all()
#     if not owners:
#         raise HTTPException(status_code=404, detail="No owners found for transfer.")
#     for owner in owners:
#         owner.village_id = request.to_village_id
#         # Update location fields if provided
#         if request.district_id is not None:
#             owner.district_id = request.district_id
#         if request.taluka_id is not None:
#             owner.taluka_id = request.taluka_id
#         if request.gram_panchayat_id is not None:
#             owner.gram_panchayat_id = request.gram_panchayat_id
        
#     db.commit()
#     return {"success": True, "transferred_owner_ids": [owner.id for owner in owners]} 

@router.post("/owners/transfer/")
def transfer_owners(request: OwnerTransferRequest, db: Session = Depends(get_db)):
    # First get all owners to transfer
    owners = db.query(Owner).filter(
        Owner.id.in_(request.owner_ids), 
        Owner.village_id == request.from_village_id
    ).all()
    
    if not owners:
        raise HTTPException(status_code=404, detail="No owners found for transfer.")

    # Get all existing anuKramank values in the target village
    existing_anukramanks = set(
        p.anuKramank for p in db.query(Property).filter(
            Property.village_id == request.to_village_id
        ).all()
    )

    properties = []
    for owner in owners:
        properties.extend(owner.properties)

    # Update owners
    for owner in owners:
        owner.village_id = request.to_village_id
        if request.district_id is not None:
            owner.district_id = request.district_id
        if request.taluka_id is not None:
            owner.taluka_id = request.taluka_id
        if request.gram_panchayat_id is not None:
            owner.gram_panchayat_id = request.gram_panchayat_id

    # Dictionary to track anukramank changes for reporting
    anukramank_changes = {}
    
    # Update properties
    for property in properties:
        if property.village_id == request.from_village_id:
            # Check if anuKramank exists in target village
            original_anukramank = property.anuKramank
            new_anukramank = original_anukramank
            
            # Keep incrementing until we find an unused anuKramank
            while new_anukramank in existing_anukramanks:
                new_anukramank += 1
            
            # Update the property's anuKramank if it changed
            if new_anukramank != original_anukramank:
                anukramank_changes[original_anukramank] = new_anukramank
                property.anuKramank = new_anukramank
            
            # Add the new anuKramank to existing set
            existing_anukramanks.add(new_anukramank)
            
            # Update location fields
            property.village_id = request.to_village_id
            if request.district_id is not None:
                property.district_id = request.district_id
            if request.taluka_id is not None:
                property.taluka_id = request.taluka_id
            if request.gram_panchayat_id is not None:
                property.gram_panchayat_id = request.gram_panchayat_id

    db.commit()
    
    return {
        "success": True, 
        "transferred_owner_ids": [owner.id for owner in owners],
        "transferred_property_count": len(properties),
        "anukramank_changes": anukramank_changes  # Report which anuKramank values were changed
    }