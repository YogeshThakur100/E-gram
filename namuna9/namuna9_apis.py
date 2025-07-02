from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
from namuna9 import namuna9_model, namuna9_schemas
from namuna9.namuna9settings import Namuna9Settings
from namuna9.namuna9_schemas import Namuna9SettingsCreate, Namuna9SettingsRead, Namuna9SettingsUpdate

router = APIRouter(
    prefix="/namuna9",
    tags=["namuna9"]
)

@router.post("/", response_model=namuna9_schemas.Namuna9YearSetupRead, status_code=status.HTTP_201_CREATED)
def create_namuna9_year_setup(setup: namuna9_schemas.Namuna9YearSetupCreate, db: Session = Depends(database.get_db)):
    # Check if a record for this village and year already exists
    existing_setup = db.query(namuna9_model.Namuna9YearSetup).filter(
        namuna9_model.Namuna9YearSetup.village == setup.village,
        namuna9_model.Namuna9YearSetup.year == setup.year
    ).first()
    if existing_setup:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A record for village '{setup.village}' and year '{setup.year}' already exists."
        )
    
    db_setup = namuna9_model.Namuna9YearSetup(**setup.dict())
    db.add(db_setup)
    db.commit()
    db.refresh(db_setup)
    return db_setup

@router.get("/list", response_model=list[namuna9_schemas.Namuna9YearSetupRead])
def list_namuna9_year_setups(db: Session = Depends(database.get_db)):
    return db.query(namuna9_model.Namuna9YearSetup).all()

@router.get("/exists")
def check_if_setup_exists(village: str, year: str, db: Session = Depends(database.get_db)):
    existing_setup = db.query(namuna9_model.Namuna9YearSetup).filter(
        namuna9_model.Namuna9YearSetup.village == village,
        namuna9_model.Namuna9YearSetup.year == year
    ).first()
    return {"exists": existing_setup is not None}

@router.post("/carry-forward")
def carry_forward_data(data: namuna9_schemas.Namuna9CarryForward, db: Session = Depends(database.get_db)):
    # This is a placeholder for the actual logic.
    # You would need to implement the business logic to:
    # 1. Find the source data from `data.from_year` for the given `data.village`.
    # 2. Select the correct values based on `data.carry_forward_option`.
    # 3. Apply these values to the `data.to_year` records for the `data.village`.
    print(f"Received carry forward request: {data}")
    return {"message": "Carry forward action received. Logic not yet implemented.", "data": data}

@router.delete("/")
def delete_namuna9_year_setup(village: str, year: str, db: Session = Depends(database.get_db)):
    db_setup = db.query(namuna9_model.Namuna9YearSetup).filter(
        namuna9_model.Namuna9YearSetup.village == village,
        namuna9_model.Namuna9YearSetup.year == year
    ).first()
    
    if not db_setup:
        raise HTTPException(status_code=404, detail=f"Setup for village '{village}' and year '{year}' not found")
    
    db.delete(db_setup)
    db.commit()
    return {"message": f"Setup for village '{village}' and year '{year}' deleted successfully."}

@router.post("/settings", response_model=Namuna9SettingsRead, status_code=status.HTTP_201_CREATED)
def create_namuna9_settings(settings: Namuna9SettingsCreate, db: Session = Depends(database.get_db)):
    db_settings = Namuna9Settings(**settings.dict())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

@router.get("/settings/{settings_id}", response_model=Namuna9SettingsRead)
def get_namuna9_settings(settings_id: str, db: Session = Depends(database.get_db)):
    db_settings = db.query(Namuna9Settings).filter(Namuna9Settings.id == settings_id).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return db_settings

@router.put("/settings/{settings_id}", response_model=Namuna9SettingsRead)
def update_namuna9_settings(settings_id: str, settings: Namuna9SettingsUpdate, db: Session = Depends(database.get_db)):
    db_settings = db.query(Namuna9Settings).filter(Namuna9Settings.id == settings_id).first()
    if not db_settings:
        # Create new row if not found (upsert)
        new_settings = Namuna9Settings(id=settings_id, **settings.dict(exclude_unset=True))
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        return new_settings
    for field, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, field, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings 