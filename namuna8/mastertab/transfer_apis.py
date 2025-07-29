from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from namuna8 import namuna8_model as models, namuna8_schemas as schemas
from database import get_db
from pydantic import BaseModel

router = APIRouter()

class TransferOwner(BaseModel):
    id: Optional[int] = None
    name: str
    wifeName: Optional[str] = None

class PropertyTransferCreate(BaseModel):
    property_id: int
    date: datetime
    entry_no: str
    transaction_date: datetime
    new_owners: List[TransferOwner]
    doc_note: Optional[str] = None
    register_note: Optional[str] = None
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None

class PropertyTransferLog(BaseModel):
    id: int
    property_id: int
    date: datetime
    entry_no: str
    transaction_date: datetime
    new_owners: List[TransferOwner]
    old_owners: List[TransferOwner]
    doc_note: Optional[str] = None
    register_note: Optional[str] = None
    created_at: datetime

@router.post('/transfer/', response_model=PropertyTransferLog)
def transfer_property(data: PropertyTransferCreate, db: Session = Depends(get_db)):
    # Get property
    prop = db.query(models.Property).filter(models.Property.anuKramank == data.property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    # Get old owners for log
    old_owners = [TransferOwner(id=o.id, name=o.name, wifeName=o.wifeName) for o in prop.owners]
    # Prepare new owners (create if needed)
    new_owners = []
    for owner in data.new_owners:
        if owner.id:
            db_owner = db.query(models.Owner).filter(models.Owner.id == owner.id).first()
            if not db_owner:
                raise HTTPException(status_code=404, detail=f"Owner with id {owner.id} not found")
        else:
            db_owner = models.Owner(
                name=owner.name, 
                wifeName=owner.wifeName, 
                village_id=prop.village_id,
                district_id=data.district_id,
                taluka_id=data.taluka_id,
                gram_panchayat_id=data.gram_panchayat_id
            )
            db.add(db_owner)
            db.commit()
            db.refresh(db_owner)
        new_owners.append(db_owner)
    # Update property owners
    prop.owners = new_owners
    db.commit()
    db.refresh(prop)
    # Log transfer (for now, just return as response; you can save to a table if needed)
    transfer_log = PropertyTransferLog(
        id=0,  # Not saved in DB, so no real ID
        property_id=prop.anuKramank,
        date=data.date,
        entry_no=data.entry_no,
        transaction_date=data.transaction_date,
        new_owners=[TransferOwner(id=o.id, name=o.name, wifeName=o.wifeName) for o in new_owners],
        old_owners=old_owners,
        doc_note=data.doc_note,
        register_note=data.register_note,
        created_at=datetime.utcnow()
    )
    return transfer_log 