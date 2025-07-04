from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .mastertabmodels import GeneralSetting, NewYojna
from .mastertabschemas import GeneralSettingCreate, GeneralSettingRead, NewYojnaCreate, NewYojnaRead
from typing import List
from uuid import UUID
from database import get_db

router = APIRouter(prefix="/master-setting", tags=["GeneralSetting"])

@router.post("/", response_model=GeneralSettingRead)
def create_or_update_general_setting(setting: GeneralSettingCreate, db: Session = Depends(get_db)):
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
def get_all_general_settings(db: Session = Depends(get_db)):
    return db.query(GeneralSetting).all()

@router.get("/{setting_id}", response_model=GeneralSettingRead)
def get_general_setting(setting_id: UUID, db: Session = Depends(get_db)):
    setting = db.query(GeneralSetting).filter(GeneralSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="GeneralSetting not found")
    return setting

@router.put("/{setting_id}", response_model=GeneralSettingRead)
def update_general_setting(setting_id: UUID, update: GeneralSettingCreate, db: Session = Depends(get_db)):
    setting = db.query(GeneralSetting).filter(GeneralSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="GeneralSetting not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(setting, key, value)
    db.commit()
    db.refresh(setting)
    return setting

@router.delete("/{setting_id}")
def delete_general_setting(setting_id: UUID, db: Session = Depends(get_db)):
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
def get_all_new_yojna(db: Session = Depends(get_db)):
    return db.query(NewYojna).all()

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