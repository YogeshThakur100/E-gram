from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
import database
from namuna8 import namuna8_model as models
from namuna8 import namuna8_schemas as schemas
from fastapi.responses import JSONResponse
from namuna8.namuna8_schemas import PropertyReportDTO
from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from namuna8.namuna8_model import Namuna8SettingTax

router = APIRouter(
    prefix="/namuna8",
    tags=["namuna8"]
)

@router.post("/", response_model=schemas.PropertyRead, status_code=status.HTTP_201_CREATED)
def create_namuna8_entry(property_data: schemas.PropertyCreate, db: Session = Depends(database.get_db)):
    owners = []
    for owner_data in property_data.owners:
        # Convert dict to Pydantic model if needed
        if isinstance(owner_data, dict):
            owner_data = schemas.OwnerCreate(**owner_data)
        db_owner = None
        if owner_data.aadhaarNumber:
            db_owner = db.query(models.Owner).filter(models.Owner.aadhaarNumber == owner_data.aadhaarNumber).first()
        if db_owner:
            # Optionally update fields if needed
            db_owner.name = owner_data.name
            if owner_data.mobileNumber is not None:
                db_owner.mobileNumber = owner_data.mobileNumber
            if owner_data.wifeName is not None:
                db_owner.wifeName = owner_data.wifeName
            if owner_data.occupantName is not None:
                db_owner.occupantName = owner_data.occupantName
            db.commit()
            owners.append(db_owner)
        else:
            new_owner = models.Owner(
                name=owner_data.name,
                aadhaarNumber=owner_data.aadhaarNumber,
                mobileNumber=owner_data.mobileNumber,
                wifeName=owner_data.wifeName,
                occupantName=owner_data.occupantName,
                ownerPhoto=getattr(owner_data, 'ownerPhoto', None),
                village_id=owner_data.village_id
            )
            db.add(new_owner)
            db.commit()
            db.refresh(new_owner)
            owners.append(new_owner)

    # --- FIX: Convert constructions dicts to model instances ---
    constructions = []
    for construction_data in property_data.constructions:
        if isinstance(construction_data, dict):
            construction_data = schemas.ConstructionCreate(**construction_data)
        construction_type = db.query(models.ConstructionType).filter_by(name=construction_data.constructionType).first()
        if not construction_type:
            raise HTTPException(status_code=400, detail=f"Invalid construction type: {construction_data.constructionType}")
        new_construction = models.Construction(
            construction_type_id=construction_type.id,
            length=construction_data.length,
            width=construction_data.width,
            constructionYear=construction_data.constructionYear,
            floor=construction_data.floor,
            bharank=construction_data.bharank,
        )
        constructions.append(new_construction)
    # --- END FIX ---

    property_dict = property_data.dict(exclude={"owners", "constructions"})
    db_property = models.Property(**property_dict, owners=owners, constructions=constructions)
    db.add(db_property)
    # Set taxes based on area and boolean fields using Namuna8SettingTax
    settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    def get_tax_by_area(area, field):
        if not settings:
            return 0
        if area is None:
            area = 0
        if area <= 300:
            return getattr(settings, field + 'Upto300', 0) or 0
        elif 301 <= area <= 700:
            return getattr(settings, field + '301_700', 0) or 0
        else:
            return getattr(settings, field + 'Above700', 0) or 0
    total_area = db_property.totalAreaSqFt or 0
    # Debug print statements
    print(f"[DEBUG] total_area: {total_area}")
    diva_kar = get_tax_by_area(total_area, 'light') if property_data.divaArogyaKar else 0
    aarogya_kar = get_tax_by_area(total_area, 'health') if property_data.divaArogyaKar else 0
    cleaning_tax = get_tax_by_area(total_area, 'cleaning') if property_data.safaiKar else 0
    toilet_tax = 0.0
    if property_data.shauchalayKar or property_data.toilet == 'आहे':
        toilet_tax = float(get_tax_by_area(total_area, 'bathroom'))
    print(f"[DEBUG] divaKar: {diva_kar}, aarogyaKar: {aarogya_kar}, cleaningTax: {cleaning_tax}, toiletTax: {toilet_tax}")
    # Assign taxes
    db_property.divaKar = diva_kar
    db_property.aarogyaKar = aarogya_kar
    db_property.cleaningTax = cleaning_tax
    if property_data.toilet == 'आहे':
        db_property.toilet = 'आहे'
        db_property.toiletTax = toilet_tax
    else:
        db_property.toilet = property_data.toilet if property_data.toilet is not None else ''
        db_property.toiletTax = 0.0
    db.commit()
    db.refresh(db_property)
    # Calculate total area if not provided
    if not db_property.totalAreaSqFt or db_property.totalAreaSqFt == 0:
        east = db_property.eastLength or 0
        west = db_property.westLength or 0
        north = db_property.northLength or 0
        south = db_property.southLength or 0
        avg_length = (east + west) / 2 if (east or west) else 0
        avg_width = (north + south) / 2 if (north or south) else 0
        db_property.totalAreaSqFt = avg_length * avg_width if avg_length and avg_width else 0
    # Build response with constructionType name
    return build_property_response(db_property, db)

@router.get("/property_list/", response_model=list[schemas.PropertyList])
def get_property_list(village: str, db: Session = Depends(database.get_db)):
    # Find the village by name
    village_obj = db.query(models.Village).filter(models.Village.name == village).first()
    if not village_obj:
        return []
    properties = db.query(models.Property).filter(models.Property.village_id == village_obj.id).all()
    result = []
    for p in properties:
        owner_name = p.owners[0].name if p.owners else "N/A"
        result.append({"malmattaKramank": p.malmattaKramank, "ownerName": owner_name, "anuKramank": p.anuKramank})
    return result

@router.get("/get-all-constructiontypes", response_model=List[schemas.ConstructionType])
def get_all_construction_types(db: Session = Depends(database.get_db)):
    return db.query(models.ConstructionType).all()

@router.get("/{anu_kramank}", response_model=schemas.PropertyRead)
def get_property_details(anu_kramank: int, db: Session = Depends(database.get_db)):
    db_property = db.query(models.Property).filter(models.Property.anuKramank == anu_kramank).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return build_property_response(db_property, db)

@router.put("/{anu_kramank}", response_model=schemas.PropertyRead)
def update_namuna8_entry(anu_kramank: int, property_data: schemas.PropertyCreate, db: Session = Depends(database.get_db)):
    db_property = db.query(models.Property).filter(models.Property.anuKramank == anu_kramank).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    property_update_data = property_data.dict(exclude={'owners', 'constructions'})
    for key, value in property_update_data.items():
        setattr(db_property, key, value)

    if property_data.owners:
        new_owners = []
        for owner_data in property_data.owners:
            # Ensure owner_data is a Pydantic model
            if isinstance(owner_data, dict):
                owner_data = schemas.OwnerCreate(**owner_data)
            owner = None
            if owner_data.aadhaarNumber:
                owner = db.query(models.Owner).filter(models.Owner.aadhaarNumber == owner_data.aadhaarNumber).first()

            if not owner:
                owner = models.Owner(
                    name=owner_data.name,
                    aadhaarNumber=owner_data.aadhaarNumber,
                    mobileNumber=owner_data.mobileNumber,
                    wifeName=owner_data.wifeName,
                    occupantName=owner_data.occupantName,
                    ownerPhoto=getattr(owner_data, 'ownerPhoto', None),
                    village_id=owner_data.village_id
                )
                db.add(owner)
                db.commit()
                db.refresh(owner)
            else:
                owner.name = owner_data.name
                if owner_data.mobileNumber is not None:
                    owner.mobileNumber = owner_data.mobileNumber
                if owner_data.wifeName is not None:
                    owner.wifeName = owner_data.wifeName
                if owner_data.occupantName is not None:
                    owner.occupantName = owner_data.occupantName
                db.commit()

            new_owners.append(owner)
        db_property.owners = new_owners

    # --- FIX: Convert constructions dicts to model instances ---
    if property_data.constructions:
        new_constructions = []
        for construction_data in property_data.constructions:
            if isinstance(construction_data, dict):
                construction_data = schemas.ConstructionCreate(**construction_data)
            construction_type = db.query(models.ConstructionType).filter_by(name=construction_data.constructionType).first()
            if not construction_type:
                raise HTTPException(status_code=400, detail=f"Invalid construction type: {construction_data.constructionType}")
            new_construction = models.Construction(
                construction_type_id=construction_type.id,
                length=construction_data.length,
                width=construction_data.width,
                constructionYear=construction_data.constructionYear,
                floor=construction_data.floor,
                bharank=construction_data.bharank,
            )
            new_constructions.append(new_construction)
        db_property.constructions = new_constructions
    # --- END FIX ---

    # Set taxes based on area and boolean fields using Namuna8SettingTax
    settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    def get_tax_by_area(area, field):
        if not settings:
            return 0
        if area is None:
            area = 0
        if area <= 300:
            return getattr(settings, field + 'Upto300', 0) or 0
        elif 301 <= area <= 700:
            return getattr(settings, field + '301_700', 0) or 0
        else:
            return getattr(settings, field + 'Above700', 0) or 0
    total_area = db_property.totalAreaSqFt or 0
    # Debug print statements
    print(f"[DEBUG] total_area: {total_area}")
    diva_kar = get_tax_by_area(total_area, 'light') if property_data.divaArogyaKar else 0
    aarogya_kar = get_tax_by_area(total_area, 'health') if property_data.divaArogyaKar else 0
    cleaning_tax = get_tax_by_area(total_area, 'cleaning') if property_data.safaiKar else 0
    toilet_tax = 0.0
    if property_data.shauchalayKar or property_data.toilet == 'आहे':
        toilet_tax = float(get_tax_by_area(total_area, 'bathroom'))
    print(f"[DEBUG] divaKar: {diva_kar}, aarogyaKar: {aarogya_kar}, cleaningTax: {cleaning_tax}, toiletTax: {toilet_tax}")
    # Assign taxes
    db_property.divaKar = diva_kar
    db_property.aarogyaKar = aarogya_kar
    db_property.cleaningTax = cleaning_tax
    if property_data.toilet == 'आहे':
        db_property.toilet = 'आहे'
        db_property.toiletTax = toilet_tax
    else:
        db_property.toilet = property_data.toilet if property_data.toilet is not None else ''
        db_property.toiletTax = 0.0

    db.commit()
    db.refresh(db_property)
    # Calculate total area if not provided
    if not db_property.totalAreaSqFt or db_property.totalAreaSqFt == 0:
        east = db_property.eastLength or 0
        west = db_property.westLength or 0
        north = db_property.northLength or 0
        south = db_property.southLength or 0
        avg_length = (east + west) / 2 if (east or west) else 0
        avg_width = (north + south) / 2 if (north or south) else 0
        db_property.totalAreaSqFt = avg_length * avg_width if avg_length and avg_width else 0
    return build_property_response(db_property, db)

@router.get("/bulk_edit_list/", response_model=list[schemas.BulkEditPropertyRow])
def get_bulk_edit_property_list(village: str, db: Session = Depends(database.get_db)):
    village_obj = db.query(models.Village).filter(models.Village.name == village).first()
    if not village_obj:
        return []
    properties = db.query(models.Property).filter(models.Property.village_id == village_obj.id).order_by(models.Property.malmattaKramank).all()
    result = []
    for idx, p in enumerate(properties, start=1):
        owner_name = p.owners[0].name if p.owners else ""
        result.append(schemas.BulkEditPropertyRow(
            serial_no=idx,
            malmattaKramank=p.malmattaKramank,
            ownerName=owner_name,
            occupant="स्वतः",  # Always 'self' for now
            gharKar=getattr(p, 'gharKar', 0),
            divaKar=getattr(p, 'divaKar', 0),
            aarogyaKar=getattr(p, 'aarogyaKar', 0),
            sapanikar=getattr(p, 'sapanikar', 0),
            vpanikar=getattr(p, 'vpanikar', 0),
        ))
    return result

@router.post("/bulk_update/")
def bulk_update_properties(update: schemas.BulkEditUpdateRequest, db: Session = Depends(database.get_db)):
    valid_water_facilities = [
        "सामान्य पाणिकर",
        "घरगुती नळ",
        "व्यावसायिक नळ",
        "कारस पात्र नसलेली इमारत",
        "सामान्य पाणिकर १ ते ३०० ची फु.",
        "सामान्य पाणिकर ३०१ ते ७०० ची फु.",
        "सामान्य पाणिकर ७०० ची फु. वरील",
        None
    ]
    updated_count = 0
    for prop_id in update.property_ids:
        prop = db.query(models.Property).filter(models.Property.malmattaKramank == prop_id).first()
        if not prop:
            continue
        # Only update fields that are not None
        if update.waterFacility1 is not None:
            if update.waterFacility1 in valid_water_facilities:
                prop.waterFacility1 = update.waterFacility1
            else:
                continue  # skip invalid value
        if update.waterFacility2 is not None:
            if update.waterFacility2 in valid_water_facilities:
                prop.waterFacility2 = update.waterFacility2
            else:
                continue  # skip invalid value
        # Set sapanikar and vpanikar based on water facilities, only if the field is being updated
        if update.waterFacility1 is not None:
            if update.waterFacility1 in ["घरगुती नळ", "व्यावसायिक नळ"]:
                prop.sapanikar = 100
            else:
                prop.sapanikar = 0
        # else: do not change sapanikar
        if update.waterFacility2 is not None:
            if update.waterFacility2 in ["घरगुती नळ", "व्यावसायिक नळ"]:
                prop.vpanikar = 100
            else:
                prop.vpanikar = 0
        # else: do not change vpanikar
        if update.toilet is not None:
            prop.toilet = update.toilet
        if update.house is not None:
            prop.house = update.house
        if update.divaArogyaKar is not None:
            prop.divaArogyaKar = update.divaArogyaKar
        if update.safaiKar is not None:
            prop.safaiKar = update.safaiKar
        if update.shauchalayKar is not None:
            prop.shauchalayKar = update.shauchalayKar
        if update.karLaguNahi is not None:
            prop.karLaguNahi = update.karLaguNahi
        updated_count += 1
    db.commit()
    return {"message": f"Updated {updated_count} properties successfully."}

# @router.get("/property_report_list/")
# def get_property_report_list(village: str, db: Session = Depends(database.get_db)):
#     properties = db.query(models.Property).filter(models.Property.villageOrMoholla == village).all()
#     rows = []
#     for prop in properties:
#         # Compose owner names
#         owner_names = []
#         for idx, owner in enumerate(prop.owners, start=1):
#             owner_names.append(f"{idx}.{owner.name}")
#         owner_name_str = ", ".join(owner_names) if owner_names else None
#         # Compose dimension string
#         dimension = None
#         if prop.eastLength or prop.westLength or prop.northLength or prop.southLength:
#             dimension = f"{prop.eastLength or ''} x {prop.westLength or ''} x {prop.northLength or ''} x {prop.southLength or ''}"
#         # Area calculation (example: product of lengths, adjust as needed)
#         area_sqft_sqm = None
#         if prop.eastLength and prop.northLength:
#             try:
#                 area_sqft = float(prop.eastLength) * float(prop.northLength)
#                 area_sqft_sqm = str(area_sqft)
#             except Exception:
#                 area_sqft_sqm = None
#         dto = PropertyReportDTO(
#             sr_no=prop.anuKramank,
#             village_info=prop.villageOrMoholla,
#             owner_name=owner_name_str,
#             occupant_name=prop.owners[0].occupantName if prop.owners and hasattr(prop.owners[0], 'occupantName') else None,
#             property_description=None,
#             property_numbers=str(prop.malmattaKramank) if prop.malmattaKramank else None,
#             dimension=dimension,
#             area_sqft_sqm=area_sqft_sqm,
#             rate_per_sqm=None,
#             depreciation_info=None,
#             tax_rate_paise=None,
#             capital_value=None,
#             tax_percentage=None,
#             tax_amount_rupees=None,
#             land_tax=None,
#             building_tax=None,
#             construction_tax=None,
#             house_tax=str(prop.gharKar) if prop.gharKar is not None else None,
#             light_tax=str(prop.divaKar) if prop.divaKar is not None else None,
#             total_tax=None
#         )
#         rows.append(dto.dict())
#     return JSONResponse(status_code=200, content={"success": True, "message": "Property report list fetched successfully", "data": rows})

@router.post("/construction_type/", response_model=schemas.ConstructionType, status_code=status.HTTP_201_CREATED)
def create_construction_type(construction_type_data: schemas.ConstructionTypeCreate, db: Session = Depends(database.get_db)):
    new_construction_type = models.ConstructionType(**construction_type_data.dict())
    db.add(new_construction_type)
    db.commit()
    db.refresh(new_construction_type)
    return new_construction_type

@router.post("/owner", status_code=status.HTTP_201_CREATED)
def create_owner(
    name: str = Body(...),
    aadhaarNumber: str = Body(...),
    mobileNumber: str = Body(...),
    villageOrMoholla: str = Body(...),
    wifeName: str = Body(None),
    db: Session = Depends(database.get_db)
):
    # Check if owner with same aadhaarNumber exists
    existing_owner = db.query(models.Owner).filter(models.Owner.aadhaarNumber == aadhaarNumber).first()
    if existing_owner:
        return {"detail": "Owner with this Aadhaar number already exists."}
    new_owner = models.Owner(
        name=name,
        aadhaarNumber=aadhaarNumber,
        mobileNumber=mobileNumber,
        wifeName=wifeName,
        villageOrMoholla=villageOrMoholla
    )
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return {
        "id": new_owner.id,
        "name": new_owner.name,
        "aadhaarNumber": new_owner.aadhaarNumber,
        "mobileNumber": new_owner.mobileNumber,
        "wifeName": new_owner.wifeName,
        "villageOrMoholla": new_owner.villageOrMoholla
    }

def build_property_response(db_property, db):
    # Build constructions with constructionType name
    constructions = []
    for c in db_property.constructions:
        constructions.append({
            "id": c.id,
            "constructionType": c.construction_type.name if c.construction_type else "",
            "length": c.length,
            "width": c.width,
            "constructionYear": c.constructionYear,
            "floor": c.floor,
            "bharank": c.bharank,
        })
    # Build owners as needed
    owners = []
    for o in db_property.owners:
        owners.append({
            "id": o.id,
            "name": o.name,
            "aadhaarNumber": o.aadhaarNumber,
            "mobileNumber": o.mobileNumber,
            "wifeName": o.wifeName,
            "occupantName": o.occupantName,
            "ownerPhoto": o.ownerPhoto,
            "village_id": o.village_id,
        })
    # Build the property dict
    property_dict = {
        **{k: getattr(db_property, k) for k in schemas.PropertyBase.__fields__.keys()},
        "owners": owners,
        "constructions": constructions,
    }
    return property_dict

# --- Namuna8SettingChecklist CRUD ---
@router.post("/settings/checklist/save", response_model=schemas.Namuna8SettingChecklistRead)
def create_checklist(data: schemas.Namuna8SettingChecklistCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == 'namuna8').first()
    if obj:
        for k, v in data.dict().items():
            setattr(obj, k, v)
    else:
        obj = models.Namuna8SettingChecklist(id='namuna8', **data.dict())
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/settings/checklist/getall", response_model=list[schemas.Namuna8SettingChecklistRead])
def get_all_checklists(db: Session = Depends(database.get_db)):
    return db.query(models.Namuna8SettingChecklist).all()

@router.get("/settings/checklist/get/{id}", response_model=schemas.Namuna8SettingChecklistRead)
def get_checklist(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return obj

@router.put("/settings/checklist/update/{id}", response_model=schemas.Namuna8SettingChecklistRead)
def update_checklist(id: str, data: schemas.Namuna8SettingChecklistCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == 'namuna8').first()
    if not obj:
        raise HTTPException(status_code=404, detail="Checklist not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/settings/checklist/delete/{id}")
def delete_checklist(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Checklist not found")
    db.delete(obj)
    db.commit()
    return {"detail": "Deleted"}

# --- Namuna8DropdownAddSettings CRUD ---
@router.post("/settings/dropdown/save", response_model=schemas.Namuna8DropdownAddSettingsRead)
def create_dropdown(data: schemas.Namuna8DropdownAddSettingsCreate, db: Session = Depends(database.get_db)):
    # anukramank_id is handled by the schema and setattr
    obj = db.query(models.Namuna8DropdownAddSettings).filter(models.Namuna8DropdownAddSettings.id == 'namuna8').first()
    if obj:
        for k, v in data.dict().items():
            setattr(obj, k, v)
    else:
        obj = models.Namuna8DropdownAddSettings(id='namuna8', **data.dict())
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/settings/dropdown/getall", response_model=list[schemas.Namuna8DropdownAddSettingsRead])
def get_all_dropdowns(db: Session = Depends(database.get_db)):
    return db.query(models.Namuna8DropdownAddSettings).all()

@router.get("/settings/dropdown/get/{id}", response_model=schemas.Namuna8DropdownAddSettingsRead)
def get_dropdown(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8DropdownAddSettings).filter(models.Namuna8DropdownAddSettings.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dropdown setting not found")
    return obj

@router.put("/settings/dropdown/update/{id}", response_model=schemas.Namuna8DropdownAddSettingsRead)
def update_dropdown(id: str, data: schemas.Namuna8DropdownAddSettingsCreate, db: Session = Depends(database.get_db)):
    # anukramank_id is handled by the schema and setattr
    obj = db.query(models.Namuna8DropdownAddSettings).filter(models.Namuna8DropdownAddSettings.id == 'namuna8').first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dropdown setting not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/settings/dropdown/delete/{id}")
def delete_dropdown(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8DropdownAddSettings).filter(models.Namuna8DropdownAddSettings.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dropdown setting not found")
    db.delete(obj)
    db.commit()
    return {"detail": "Deleted"}

# --- Namuna8SettingTax CRUD ---
@router.post("/settings/tax/save", response_model=schemas.Namuna8SettingTaxRead)
def create_tax(data: schemas.Namuna8SettingTaxCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    if obj:
        for k, v in data.dict().items():
            setattr(obj, k, v)
    else:
        obj = models.Namuna8SettingTax(id='namuna8', **data.dict())
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/settings/tax/getall", response_model=list[schemas.Namuna8SettingTaxRead])
def get_all_taxes(db: Session = Depends(database.get_db)):
    return db.query(models.Namuna8SettingTax).all()

@router.get("/settings/tax/get/{id}", response_model=schemas.Namuna8SettingTaxRead)
def get_tax(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tax setting not found")
    return obj

@router.put("/settings/tax/update/{id}", response_model=schemas.Namuna8SettingTaxRead)
def update_tax(id: str, data: schemas.Namuna8SettingTaxCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tax setting not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/settings/tax/delete/{id}")
def delete_tax(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tax setting not found")
    db.delete(obj)
    db.commit()
    return {"detail": "Deleted"}

# --- Namuna8WaterTaxSettings CRUD ---
@router.post("/settings/watertax/save", response_model=schemas.Namuna8WaterTaxSettingsRead)
def create_watertax(data: schemas.Namuna8WaterTaxSettingsCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == 'namuna8').first()
    if obj:
        for k, v in data.dict().items():
            setattr(obj, k, v)
    else:
        obj = models.Namuna8WaterTaxSettings(id='namuna8', **data.dict())
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/settings/watertax/getall", response_model=list[schemas.Namuna8WaterTaxSettingsRead])
def get_all_watertax(db: Session = Depends(database.get_db)):
    return db.query(models.Namuna8WaterTaxSettings).all()

@router.get("/settings/watertax/get/{id}", response_model=schemas.Namuna8WaterTaxSettingsRead)
def get_watertax(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Water tax setting not found")
    return obj

@router.put("/settings/watertax/update/{id}", response_model=schemas.Namuna8WaterTaxSettingsRead)
def update_watertax(id: str, data: schemas.Namuna8WaterTaxSettingsCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == 'namuna8').first()
    if not obj:
        raise HTTPException(status_code=404, detail="Water tax setting not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/settings/watertax/delete/{id}")
def delete_watertax(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Water tax setting not found")
    db.delete(obj)
    db.commit()
    return {"detail": "Deleted"}

# --- Namuna8GeneralWaterTaxSlabSettings CRUD ---
@router.post("/settings/watertaxslab/save", response_model=schemas.Namuna8GeneralWaterTaxSlabSettingsRead)
def create_watertaxslab(data: schemas.Namuna8GeneralWaterTaxSlabSettingsCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8GeneralWaterTaxSlabSettings).filter(models.Namuna8GeneralWaterTaxSlabSettings.id == 'namuna8').first()
    if obj:
        for k, v in data.dict().items():
            setattr(obj, k, v)
    else:
        obj = models.Namuna8GeneralWaterTaxSlabSettings(id='namuna8', **data.dict())
        db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/settings/watertaxslab/getall", response_model=list[schemas.Namuna8GeneralWaterTaxSlabSettingsRead])
def get_all_watertaxslab(db: Session = Depends(database.get_db)):
    return db.query(models.Namuna8GeneralWaterTaxSlabSettings).all()

@router.get("/settings/watertaxslab/get/{id}", response_model=schemas.Namuna8GeneralWaterTaxSlabSettingsRead)
def get_watertaxslab(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8GeneralWaterTaxSlabSettings).filter(models.Namuna8GeneralWaterTaxSlabSettings.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Water tax slab setting not found")
    return obj

@router.put("/settings/watertaxslab/update/{id}", response_model=schemas.Namuna8GeneralWaterTaxSlabSettingsRead)
def update_watertaxslab(id: str, data: schemas.Namuna8GeneralWaterTaxSlabSettingsCreate, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8GeneralWaterTaxSlabSettings).filter(models.Namuna8GeneralWaterTaxSlabSettings.id == 'namuna8').first()
    if not obj:
        raise HTTPException(status_code=404, detail="Water tax slab setting not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/settings/watertaxslab/delete/{id}")
def delete_watertaxslab(id: str, db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8GeneralWaterTaxSlabSettings).filter(models.Namuna8GeneralWaterTaxSlabSettings.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Water tax slab setting not found")
    db.delete(obj)
    db.commit()
    return {"detail": "Deleted"}

@router.post("/construction_type/bulk_upsert", response_model=List[schemas.ConstructionType])
def bulk_upsert_construction_types(request: schemas.BulkConstructionTypeUpsertRequest, db: Session = Depends(database.get_db)):
    result = []
    for item in request.construction_types:
        if item.id is not None:
            obj = db.query(models.ConstructionType).filter(models.ConstructionType.id == item.id).first()
            if obj:
                obj.name = item.name
                obj.rate = item.rate
                obj.bandhmastache_dar = item.bandhmastache_dar
                obj.bandhmastache_prakar = item.bandhmastache_prakar
                obj.gharache_prakar = item.gharache_prakar
                db.commit()
                db.refresh(obj)
                result.append(obj)
            else:
                # If id is given but not found, create new
                new_obj = models.ConstructionType(
                    name=item.name,
                    rate=item.rate,
                    bandhmastache_dar=item.bandhmastache_dar,
                    bandhmastache_prakar=item.bandhmastache_prakar,
                    gharache_prakar=item.gharache_prakar
                )
                db.add(new_obj)
                db.commit()
                db.refresh(new_obj)
                result.append(new_obj)
        else:
            new_obj = models.ConstructionType(
                name=item.name,
                rate=item.rate,
                bandhmastache_dar=item.bandhmastache_dar,
                bandhmastache_prakar=item.bandhmastache_prakar,
                gharache_prakar=item.gharache_prakar
            )
            db.add(new_obj)
            db.commit()
            db.refresh(new_obj)
            result.append(new_obj)
    return result

@router.post("/settings/bulk_save")
def bulk_save_namuna8_settings(request: schemas.BulkNamuna8SettingsRequest, db: Session = Depends(database.get_db)):
    result = {}
    # Checklist
    if request.checklist:
        checklist_id = request.checklist.id or 'namuna8'
        checklist_obj = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == checklist_id).first()
        if checklist_obj:
            for k, v in request.checklist.dict(exclude_unset=True, exclude={'id'}).items():
                setattr(checklist_obj, k, v)
        else:
            checklist_obj = models.Namuna8SettingChecklist(id=checklist_id, **request.checklist.dict(exclude_unset=True, exclude={'id'}))
            db.add(checklist_obj)
        db.commit()
        db.refresh(checklist_obj)
        result['checklist'] = checklist_obj
    # Dropdown
    if request.dropdown:
        dropdown_data = request.dropdown.dict(exclude_unset=True)
        dropdown_data.pop('id', None)
        obj = db.query(models.Namuna8DropdownAddSettings).filter(models.Namuna8DropdownAddSettings.id == 'namuna8').first()
        if obj:
            for k, v in dropdown_data.items():
                setattr(obj, k, v)
        else:
            obj = models.Namuna8DropdownAddSettings(id='namuna8', **dropdown_data)
            db.add(obj)
        db.commit()
        db.refresh(obj)
        result['dropdown'] = obj
    # Tax
    if request.tax:
        tax_data = request.tax.dict(exclude_unset=True)
        tax_data.pop('id', None)
        tax_obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
        if tax_obj:
            for k, v in tax_data.items():
                setattr(tax_obj, k, v)
        else:
            tax_obj = models.Namuna8SettingTax(id='namuna8', **tax_data)
            db.add(tax_obj)
        db.commit()
        db.refresh(tax_obj)
        result['tax'] = tax_obj
    # Water Tax
    if request.watertax:
        watertax_data = request.watertax.dict(exclude_unset=True)
        watertax_data.pop('id', None)
        watertax_obj = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == 'namuna8').first()
        if watertax_obj:
            for k, v in watertax_data.items():
                setattr(watertax_obj, k, v)
        else:
            watertax_obj = models.Namuna8WaterTaxSettings(id='namuna8', **watertax_data)
            db.add(watertax_obj)
        db.commit()
        db.refresh(watertax_obj)
        result['watertax'] = watertax_obj
    # Water Tax Slab
    if request.watertaxslab:
        watertaxslab_data = request.watertaxslab.dict(exclude_unset=True)
        watertaxslab_data.pop('id', None)
        watertaxslab_obj = db.query(models.Namuna8GeneralWaterTaxSlabSettings).filter(models.Namuna8GeneralWaterTaxSlabSettings.id == 'namuna8').first()
        if watertaxslab_obj:
            for k, v in watertaxslab_data.items():
                setattr(watertaxslab_obj, k, v)
        else:
            watertaxslab_obj = models.Namuna8GeneralWaterTaxSlabSettings(id='namuna8', **watertaxslab_data)
            db.add(watertaxslab_obj)
        db.commit()
        db.refresh(watertaxslab_obj)
        result['watertaxslab'] = watertaxslab_obj
    # Construction Types bulk upsert
    if request.construction_types:
        result_construction_types = []
        for item in request.construction_types:
            if item.id is not None:
                obj = db.query(models.ConstructionType).filter(models.ConstructionType.id == item.id).first()
                if obj:
                    obj.name = item.name
                    obj.rate = item.rate
                    obj.bandhmastache_dar = item.bandhmastache_dar
                    obj.bandhmastache_prakar = item.bandhmastache_prakar
                    obj.gharache_prakar = item.gharache_prakar
                    db.commit()
                    db.refresh(obj)
                    result_construction_types.append(obj)
                else:
                    new_obj = models.ConstructionType(
                        name=item.name,
                        rate=item.rate,
                        bandhmastache_dar=item.bandhmastache_dar,
                        bandhmastache_prakar=item.bandhmastache_prakar,
                        gharache_prakar=item.gharache_prakar
                    )
                    db.add(new_obj)
                    db.commit()
                    db.refresh(new_obj)
                    result_construction_types.append(new_obj)
            else:
                new_obj = models.ConstructionType(
                    name=item.name,
                    rate=item.rate,
                    bandhmastache_dar=item.bandhmastache_dar,
                    bandhmastache_prakar=item.bandhmastache_prakar,
                    gharache_prakar=item.gharache_prakar
                )
                db.add(new_obj)
                db.commit()
                db.refresh(new_obj)
                result_construction_types.append(new_obj)
        result['construction_types'] = result_construction_types
    return result

# --- Village CRUD Operations ---
@router.post("/village/", response_model=schemas.VillageRead, status_code=status.HTTP_201_CREATED)
def create_village(village_data: schemas.VillageCreate, db: Session = Depends(database.get_db)):
    # Check if village with same name already exists
    existing_village = db.query(models.Village).filter(models.Village.name == village_data.name).first()
    if existing_village:
        raise HTTPException(status_code=400, detail="Village with this name already exists")
    
    new_village = models.Village(**village_data.dict())
    db.add(new_village)
    db.commit()
    db.refresh(new_village)
    return new_village

@router.get("/village/", response_model=List[schemas.VillageRead])
def get_all_villages(db: Session = Depends(database.get_db)):
    return db.query(models.Village).all()

@router.get("/village/{village_id}", response_model=schemas.VillageRead)
def get_village(village_id: int, db: Session = Depends(database.get_db)):
    village = db.query(models.Village).filter(models.Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return village

@router.get("/village/name/{village_name}", response_model=schemas.VillageRead)
def get_village_by_name(village_name: str, db: Session = Depends(database.get_db)):
    village = db.query(models.Village).filter(models.Village.name == village_name).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return village

@router.put("/village/{village_id}", response_model=schemas.VillageRead)
def update_village(village_id: int, village_data: schemas.VillageCreate, db: Session = Depends(database.get_db)):
    village = db.query(models.Village).filter(models.Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    
    # Check if new name conflicts with existing village
    if village_data.name != village.name:
        existing_village = db.query(models.Village).filter(models.Village.name == village_data.name).first()
        if existing_village:
            raise HTTPException(status_code=400, detail="Village with this name already exists")
    
    for key, value in village_data.dict().items():
        setattr(village, key, value)
    
    village.updated_at = datetime.now()
    db.commit()
    db.refresh(village)
    return village

@router.delete("/village/{village_id}")
def delete_village(village_id: int, db: Session = Depends(database.get_db)):
    village = db.query(models.Village).filter(models.Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    
    # Check if village has associated properties or owners
    if village.properties or village.owners:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete village that has associated properties or owners. Please delete all properties and owners first."
        )
    
    db.delete(village)
    db.commit()
    return {"message": "Village deleted successfully"}

@router.post("/village/bulk", response_model=List[schemas.VillageRead], status_code=status.HTTP_201_CREATED)
def create_bulk_villages(villages: List[schemas.VillageCreate], db: Session = Depends(database.get_db)):
    created_villages = []
    for village_data in villages:
        # Check if village with same name already exists
        existing_village = db.query(models.Village).filter(models.Village.name == village_data.name).first()
        if existing_village:
            continue  # Skip duplicates
        new_village = models.Village(**village_data.dict())
        db.add(new_village)
        db.commit()
        db.refresh(new_village)
        created_villages.append(new_village)
    return created_villages

@router.get("/owners/", response_model=List[schemas.Owner])
def get_all_owners(db: Session = Depends(database.get_db)):
    return db.query(models.Owner).all()

@router.get("/properties_by_village/", response_model=List[schemas.PropertyRead])
def get_properties_by_village(village_id: int, db: Session = Depends(database.get_db)):
    properties = db.query(models.Property).filter(models.Property.village_id == village_id).all()
    return [build_property_response(p, db) for p in properties]

def get_tax_rate_by_area(db: Session, area: float, field: str):
    # Fetch the first settings row (assuming only one row for now)
    settings = db.query(Namuna8SettingTax).first()
    if not settings:
        return 0
    if area <= 300:
        return getattr(settings, field + 'Upto300', 0)
    elif 301 <= area <= 700:
        return getattr(settings, field + '301_700', 0)
    else:
        return getattr(settings, field + 'Above700', 0)

@router.post("/admin/recalculate_taxes", status_code=200)
def recalculate_all_property_taxes(db: Session = Depends(database.get_db)):
    settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    if not settings:
        return {"detail": "No settings found"}
    def get_tax_by_area(area, field):
        if area is None:
            area = 0
        if area <= 300:
            return getattr(settings, field + 'Upto300', 0) or 0
        elif 301 <= area <= 700:
            return getattr(settings, field + '301_700', 0) or 0
        else:
            return getattr(settings, field + 'Above700', 0) or 0
    properties = db.query(models.Property).all()
    for prop in properties:
        total_area = prop.totalAreaSqFt or 0
        prop.divaKar = get_tax_by_area(total_area, 'light') if prop.divaArogyaKar else 0
        prop.aarogyaKar = get_tax_by_area(total_area, 'health') if prop.divaArogyaKar else 0
        prop.cleaningTax = get_tax_by_area(total_area, 'cleaning') if prop.safaiKar else 0
        if prop.toilet == 'आहे':
            prop.toiletTax = float(get_tax_by_area(total_area, 'bathroom'))
        else:
            prop.toiletTax = 0.0
    db.commit()
    return {"detail": "All property taxes recalculated and updated."}
    