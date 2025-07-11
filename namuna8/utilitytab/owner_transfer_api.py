from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from ..namuna8_model import Owner

from pydantic import BaseModel

router = APIRouter()

class OwnerTransferRequest(BaseModel):
    from_village_id: int
    to_village_id: int
    owner_ids: List[int]

@router.post("/owners/transfer/")
def transfer_owners(request: OwnerTransferRequest, db: Session = Depends(get_db)):
    owners = db.query(Owner).filter(Owner.id.in_(request.owner_ids), Owner.village_id == request.from_village_id).all()
    if not owners:
        raise HTTPException(status_code=404, detail="No owners found for transfer.")
    for owner in owners:
        owner.village_id = request.to_village_id
    db.commit()
    return {"success": True, "transferred_owner_ids": [owner.id for owner in owners]} 