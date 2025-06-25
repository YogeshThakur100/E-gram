from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
from namuna8 import namuna8_model as models
from namuna8 import namuna8_schemas as schemas
from fastapi.responses import JSONResponse
from namuna8.namuna8_schemas import PropertyReportDTO

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
        new_construction = models.Construction(
            constructionType=construction_data.constructionType,
            length=construction_data.length,
            width=construction_data.width,
            constructionYear=construction_data.constructionYear,
            floor=construction_data.floor,
            usage=construction_data.usage,
            bharank=construction_data.bharank,
        )
        constructions.append(new_construction)
    # --- END FIX ---

    property_dict = property_data.dict(exclude={"owners", "constructions"})
    db_property = models.Property(**property_dict, owners=owners, constructions=constructions)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.get("/property_list/", response_model=list[schemas.PropertyList])
def get_property_list(village: str, db: Session = Depends(database.get_db)):
    properties = db.query(models.Property).filter(models.Property.villageOrMoholla == village).all()
    result = []
    for p in properties:
        owner_name = p.owners[0].name if p.owners else "N/A"
        result.append({"malmattaKramank": p.malmattaKramank, "ownerName": owner_name, "anuKramank": p.anuKramank})
    return result

@router.get("/{anu_kramank}", response_model=schemas.PropertyRead)
def get_property_details(anu_kramank: int, db: Session = Depends(database.get_db)):
    db_property = db.query(models.Property).filter(models.Property.anuKramank == anu_kramank).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

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
                owner = models.Owner(**owner_data.dict())
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
            new_construction = models.Construction(
                constructionType=construction_data.constructionType,
                length=construction_data.length,
                width=construction_data.width,
                constructionYear=construction_data.constructionYear,
                floor=construction_data.floor,
                usage=construction_data.usage,
                bharank=construction_data.bharank,
            )
            new_constructions.append(new_construction)
        db_property.constructions = new_constructions
    # --- END FIX ---

    db.commit()
    db.refresh(db_property)
    return db_property

@router.get("/bulk_edit_list/", response_model=list[schemas.BulkEditPropertyRow])
def get_bulk_edit_property_list(village: str, db: Session = Depends(database.get_db)):
    properties = db.query(models.Property).filter(models.Property.villageOrMoholla == village).order_by(models.Property.malmattaKramank).all()
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
    updated_count = 0
    for prop_id in update.property_ids:
        prop = db.query(models.Property).filter(models.Property.malmattaKramank == prop_id).first()
        if not prop:
            continue
        # Only update fields that are not None
        if update.waterFacility1 is not None:
            prop.waterFacility1 = update.waterFacility1
        if update.waterFacility2 is not None:
            prop.waterFacility2 = update.waterFacility2
        # Set sapanikar based on water facility
        if (getattr(update, 'waterFacility1', None) in ["घरगुती नळ", "व्यावसायिक नळ"] or getattr(update, 'waterFacility2', None) in ["घरगुती नळ", "व्यावसायिक नळ"]):
            prop.sapanikar = 100
        else:
            prop.sapanikar = 0
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

@router.get("/property_report_list/")
def get_property_report_list(village: str, db: Session = Depends(database.get_db)):
    properties = db.query(models.Property).filter(models.Property.villageOrMoholla == village).all()
    rows = []
    for prop in properties:
        # Compose owner names
        owner_names = []
        for idx, owner in enumerate(prop.owners, start=1):
            owner_names.append(f"{idx}.{owner.name}")
        owner_name_str = ", ".join(owner_names) if owner_names else None
        # Compose dimension string
        dimension = None
        if prop.eastLength or prop.westLength or prop.northLength or prop.southLength:
            dimension = f"{prop.eastLength or ''} x {prop.westLength or ''} x {prop.northLength or ''} x {prop.southLength or ''}"
        # Area calculation (example: product of lengths, adjust as needed)
        area_sqft_sqm = None
        if prop.eastLength and prop.northLength:
            try:
                area_sqft = float(prop.eastLength) * float(prop.northLength)
                area_sqft_sqm = str(area_sqft)
            except Exception:
                area_sqft_sqm = None
        dto = PropertyReportDTO(
            sr_no=prop.anuKramank,
            village_info=prop.villageOrMoholla,
            owner_name=owner_name_str,
            occupant_name=prop.owners[0].occupantName if prop.owners and hasattr(prop.owners[0], 'occupantName') else None,
            property_description=None,
            property_numbers=str(prop.malmattaKramank) if prop.malmattaKramank else None,
            dimension=dimension,
            area_sqft_sqm=area_sqft_sqm,
            rate_per_sqm=None,
            depreciation_info=None,
            usage_factor=prop.constructions[0].usage if prop.constructions else None,
            tax_rate_paise=None,
            capital_value=None,
            tax_percentage=None,
            tax_amount_rupees=None,
            land_tax=None,
            building_tax=None,
            construction_tax=None,
            house_tax=str(prop.gharKar) if prop.gharKar is not None else None,
            light_tax=str(prop.divaKar) if prop.divaKar is not None else None,
            total_tax=None
        )
        rows.append(dto.dict())
    return JSONResponse(status_code=200, content={"success": True, "message": "Property report list fetched successfully", "data": rows})