from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
from namuna9 import namuna9_model, namuna9_schemas
from namuna9.namuna9settings import Namuna9Settings
from namuna9.namuna9_schemas import Namuna9SettingsCreate, Namuna9SettingsRead, Namuna9SettingsUpdate
from namuna8 import namuna8_model
from sqlalchemy.exc import IntegrityError
from namuna8.namuna8_apis import build_property_response

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
    db_record = db.query(namuna9_model.Namuna9).filter(
        namuna9_model.Namuna9.villageId == village,
        namuna9_model.Namuna9.yearslap == year
    ).first()
    if not db_record:
        raise HTTPException(status_code=404, detail=f"Record for village '{village}' and year '{year}' not found")
    db.delete(db_record)
    db.commit()
    return {"message": f"Record for village '{village}' and year '{year}' deleted successfully."}

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

@router.post("/create-or-carry-forward")
def create_or_carry_forward_namuna9(
    payload: dict, db: Session = Depends(database.get_db)
):
    village = payload.get("village")
    yearslap = payload.get("yearslap")
    data_source = payload.get("data_source")
    grampanchayatId = payload.get("grampanchayatId")
    if not (village and yearslap and data_source):
        raise HTTPException(status_code=400, detail="Missing required fields.")

    # Check for existing (villageId, yearslap) pair
    existing = db.query(namuna9_model.Namuna9).filter(
        namuna9_model.Namuna9.villageId == village,
        namuna9_model.Namuna9.yearslap == yearslap
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="A record for this village and year already exists. Please delete it first if you want to replace it.")

    if data_source == "जुना नमुना ९ मधून डाटा घेणे":
        # Find previous year
        try:
            prev_year = str(int(yearslap.split("-")[0]) - 1) + "-" + str(int(yearslap.split("-")[1]) - 1)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid yearslap format.")
        prev_records = []
        while int(prev_year.split("-")[0]) > 2000:
            prev_records = db.query(namuna9_model.Namuna9).filter(
                namuna9_model.Namuna9.villageId == village,
                namuna9_model.Namuna9.yearslap == prev_year
            ).all()
            if prev_records:
                break
            prev_year = str(int(prev_year.split("-")[0]) - 1) + "-" + str(int(prev_year.split("-")[1]) - 1)
        if not prev_records:
            raise HTTPException(status_code=404, detail="No previous Namuna9 records found for this village.")
        # Collect all property IDs from previous Namuna9 records
        prev_property_ids = set()
        for rec in prev_records:
            if getattr(rec, 'property_ids', None) and isinstance(rec.property_ids, list):
                prev_property_ids.update(rec.property_ids)
        # Get all property IDs for the given village for the current year (yearslap)
        start_year = int(yearslap.split('-')[0])
        current_year_properties = db.query(namuna8_model.Property).filter(
            namuna8_model.Property.village_id == village,
            namuna8_model.Property.created_at != None
        ).all()
        current_year_property_ids = [p.anuKramank for p in current_year_properties if p.created_at.year == start_year]
        # Combine all property IDs (avoid duplicates)
        all_property_ids = list(set(list(prev_property_ids) + current_year_property_ids))
        # Create new Namuna9 record for this yearslap
        new_namuna9 = namuna9_model.Namuna9(
            yearslap=yearslap,
            villageId=village,
            grampanchayatId=grampanchayatId,
            property_ids=all_property_ids
        )
        try:
            db.add(new_namuna9)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="A record for this year already exists. Please delete it first if you want to replace it.")
        return {"message": "Carry forward successful."}
    elif data_source == "नवीन बनवा":
        # Get all property IDs for the given village (ignore year)
        properties = db.query(namuna8_model.Property).filter(
            namuna8_model.Property.village_id == village
        ).all()
        property_ids = [p.anuKramank for p in properties]
        new_namuna9 = namuna9_model.Namuna9(
            yearslap=yearslap,
            villageId=village,
            grampanchayatId=grampanchayatId,
            property_ids=property_ids
        )
        try:
            db.add(new_namuna9)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="A record for this year already exists. Please delete it first if you want to replace it.")
        return {"message": "New Namuna9 record created."}
    else:
        raise HTTPException(status_code=400, detail="Invalid data_source value.") 

@router.get("/list-all")
def list_all_namuna9(db: Session = Depends(database.get_db)):
    records = db.query(namuna9_model.Namuna9).all()
    # Return as dicts for easier inspection
    return [
        {
            "id": r.id,
            "yearslap": r.yearslap,
            "villageId": r.villageId,
            "grampanchayatId": r.grampanchayatId,
            "property_ids": r.property_ids,
            "createdAt": r.createdAt,
            "updatedAt": r.updatedAt
        }
        for r in records
    ] 

@router.get("/delete-options")
def get_delete_options(db: Session = Depends(database.get_db)):
    # Get all unique villageIds and yearslaps from Namuna9
    records = db.query(namuna9_model.Namuna9).all()
    unique_village_ids = set()
    unique_years = set()
    pairs = []
    for r in records:
        unique_village_ids.add(r.villageId)
        unique_years.add(r.yearslap)
        pairs.append({"villageId": str(r.villageId), "yearslap": r.yearslap})
    # Get village names for these IDs
    villages = db.query(namuna8_model.Village).filter(namuna8_model.Village.id.in_(unique_village_ids)).all()
    village_list = [{"id": v.id, "name": v.name} for v in villages]
    return {"villages": village_list, "years": sorted(list(unique_years)), "pairs": pairs} 

@router.get("/table-data")
def get_namuna9_table_data(villageId: str, yearslap: str, db: Session = Depends(database.get_db)):
    # Find the Namuna9 record for this village and year
    rec = db.query(namuna9_model.Namuna9).filter(
        namuna9_model.Namuna9.villageId == villageId,
        namuna9_model.Namuna9.yearslap == yearslap
    ).first()
    if not rec:
        return []
    property_ids = getattr(rec, 'property_ids', None)
    if not isinstance(property_ids, list) or len(property_ids) == 0:
        return []
    # Fetch all property details
    properties = db.query(namuna8_model.Property).filter(namuna8_model.Property.anuKramank.in_([int(i) for i in property_ids])).all()
    rows = []
    for idx, prop in enumerate(properties, 1):
        prop_data = build_property_response(prop, db)
        # Query constructions directly for this property
        constructions = db.query(namuna8_model.Construction).filter(
            namuna8_model.Construction.property_anuKramank == prop.anuKramank
        ).all()
        totalHouseTax = sum([c.houseTax or 0 for c in constructions])
        # Join all owner names
        owner_names = ', '.join([o.get('name', '') for o in prop_data.get('owners', [])])
        # lightingTax, healthTax, sapanikar, vpanikar, cleaningTax
        lightingTax = prop_data.get('divaKar', 0) or 0
        healthTax = prop_data.get('aarogyaKar', 0) or prop_data.get('healthTax', 0) or 0
        sapanikar = prop_data.get('sapanikar', 0) or 0
        vpanikar = prop_data.get('vpanikar', 0) or 0
        cleaningTax = prop_data.get('cleaningTax', 0) or 0
        # Total lightingTax, healthTax, sapanikar, vpanikar, cleaningTax are same as their respective fields
        # Total = sum of all numeric columns except serial, property no, owner name
        total = (
            0 + 0 + totalHouseTax + totalHouseTax + 0 + lightingTax + lightingTax + 0 + healthTax + healthTax + 0 + sapanikar + sapanikar + 0 + vpanikar + vpanikar + 0 + cleaningTax + cleaningTax + 0 + 0
        )
        row = {
            "anukramk": idx,
            "malmattaKramank": prop_data.get('malmattaKramank', ''),
            "ownerNames": owner_names,
            "shaktiGhar": 0,
            "dand": 0,
            "chaluGhar": totalHouseTax,
            "ekunGhar": totalHouseTax,
            "totalHouseTax": totalHouseTax,
            "shaktiDiva": 0,
            "chaluDiva": lightingTax,
            "ekunDiva": lightingTax,
            "shaktiAarogyaKar": 0,
            "chaluAarogyaKar": healthTax,
            "ekunAarogyaKar": healthTax,
            "shaktiSapanikar": 0,
            "chaluSapanikar": sapanikar,
            "ekunSapanikar": sapanikar,
            "shaktiVpanikar": 0,
            "chaluVpanikar": vpanikar,
            "ekunVpanikar": vpanikar,
            "shaktiCleaningTax": 0,
            "chaluCleaningTax": cleaningTax,
            "ekunCleaningTax": cleaningTax,
            "warrantFee": 0,
            "noticeFee": 0,
            "total": total
        }
        rows.append(row)
    return rows 