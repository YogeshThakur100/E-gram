from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .mastertabmodels import GeneralSetting, NewYojna
from .mastertabschemas import GeneralSettingCreate, GeneralSettingRead, NewYojnaCreate, NewYojnaRead
from typing import List
from uuid import UUID
from database import get_db
from namuna8.namuna8_model import Owner
from pydantic import BaseModel

router = APIRouter(prefix="/master-setting", tags=["GeneralSetting"])

@router.post("/", response_model=GeneralSettingRead)
def create_or_update_general_setting(setting: GeneralSettingCreate, db: Session = Depends(get_db)):
    # If no ID provided, use gram_panchayat_id as the ID
    if not setting.id and setting.gram_panchayat_id:
        setting.id = f"namuna8_{setting.gram_panchayat_id}"
    elif not setting.id:
        raise HTTPException(status_code=400, detail="Either id or gram_panchayat_id must be provided")
    
    db_setting = db.query(GeneralSetting).filter(GeneralSetting.id == setting.id).first()
    if db_setting:
        # Update existing
        for key, value in setting.dict(exclude_unset=True).items():
            setattr(db_setting, key, value)
        db.commit()
        db.refresh(db_setting)
        return db_setting
    else:
        # Create new
        db_setting = GeneralSetting(**setting.dict())
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        return db_setting

@router.get("/", response_model=List[GeneralSettingRead])
def get_all_general_settings(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(GeneralSetting)
    if district_id:
        query = query.filter(GeneralSetting.district_id == district_id)
    if taluka_id:
        query = query.filter(GeneralSetting.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(GeneralSetting.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get("/{setting_id}", response_model=GeneralSettingRead)
def get_general_setting(setting_id: str, db: Session = Depends(get_db)):
    setting = db.query(GeneralSetting).filter(GeneralSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="GeneralSetting not found")
    return setting

@router.put("/{setting_id}", response_model=GeneralSettingRead)
def update_general_setting(setting_id: str, update: GeneralSettingCreate, db: Session = Depends(get_db)):
    setting = db.query(GeneralSetting).filter(GeneralSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="GeneralSetting not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(setting, key, value)
    db.commit()
    db.refresh(setting)
    return setting

@router.delete("/{setting_id}")
def delete_general_setting(setting_id: str, db: Session = Depends(get_db)):
    setting = db.query(GeneralSetting).filter(GeneralSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="GeneralSetting not found")
    db.delete(setting)
    db.commit()
    return {"detail": "Deleted successfully"}

# --- NewYojna CRUD API ---
@router.post('/new-yojna/', response_model=NewYojnaRead)
def create_new_yojna(yojna: NewYojnaCreate, db: Session = Depends(get_db)):
    db_yojna = NewYojna(**yojna.dict())
    db.add(db_yojna)
    db.commit()
    db.refresh(db_yojna)
    return db_yojna

@router.get('/new-yojna/', response_model=List[NewYojnaRead])
def get_all_new_yojna(
    district_id: int = None,
    taluka_id: int = None,
    gram_panchayat_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(NewYojna)
    if district_id:
        query = query.filter(NewYojna.district_id == district_id)
    if taluka_id:
        query = query.filter(NewYojna.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(NewYojna.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get('/new-yojna/{yojna_id}', response_model=NewYojnaRead)
def get_new_yojna(yojna_id: int, db: Session = Depends(get_db)):
    yojna = db.query(NewYojna).filter(NewYojna.id == yojna_id).first()
    if not yojna:
        raise HTTPException(status_code=404, detail="Yojna not found")
    return yojna

@router.put('/new-yojna/{yojna_id}', response_model=NewYojnaRead)
def update_new_yojna(yojna_id: int, update: NewYojnaCreate, db: Session = Depends(get_db)):
    yojna = db.query(NewYojna).filter(NewYojna.id == yojna_id).first()
    if not yojna:
        raise HTTPException(status_code=404, detail="Yojna not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(yojna, key, value)
    db.commit()
    db.refresh(yojna)
    return yojna

@router.delete('/new-yojna/{yojna_id}')
def delete_new_yojna(yojna_id: int, db: Session = Depends(get_db)):
    yojna = db.query(NewYojna).filter(NewYojna.id == yojna_id).first()
    if not yojna:
        raise HTTPException(status_code=404, detail="Yojna not found")
    db.delete(yojna)
    db.commit()
    return {"detail": "Deleted successfully"}

class SetHolderNoRequest(BaseModel):
    owner_id: int
    holderno: int

@router.post('/set-holderno/')
def set_holderno(data: SetHolderNoRequest, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == data.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    owner.holderno = data.holderno
    db.commit()
    db.refresh(owner)
    return {"detail": "Holder number updated successfully", "owner_id": owner.id, "holderno": owner.holderno} 