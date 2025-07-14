from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
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
from sqlalchemy.exc import SQLAlchemyError
from namuna8.calculations.naumuna8_calculations import calculate_depreciation_rate


router = APIRouter(
    prefix="/namuna8",
    tags=["namuna8"]
)

@router.post("/", response_model=schemas.PropertyRead, status_code=status.HTTP_201_CREATED)
def create_namuna8_entry(property_data: schemas.PropertyCreate, db: Session = Depends(database.get_db)):
    try:
        with db.begin():
            owners = []
            for owner_data in property_data.owners:
                # Convert dict to Pydantic model if needed
                if isinstance(owner_data, dict):
                    owner_data = schemas.OwnerCreate(**owner_data)
                db_owner = None
                owner_id = getattr(owner_data, 'id', None)
                if owner_id:
                    db_owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
                elif owner_data.aadhaarNumber:
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
                    db.flush()
                    owners.append(db_owner)
                else:
                    new_owner = models.Owner(
                        name=owner_data.name,
                        aadhaarNumber=owner_data.aadhaarNumber,
                        mobileNumber=owner_data.mobileNumber,
                        wifeName=owner_data.wifeName,
                        occupantName=owner_data.occupantName,
                        ownerPhoto=getattr(owner_data, 'ownerPhoto', None) if getattr(owner_data, 'ownerPhoto', None) is not None and isinstance(getattr(owner_data, 'ownerPhoto', None), str) and getattr(owner_data, 'ownerPhoto', None) != '' else None,
                        village_id=owner_data.village_id
                    )
                    new_owner.created_at = datetime.now()
                    db.add(new_owner)
                    db.flush()
                    owners.append(new_owner)

            # --- FIX: Convert constructions dicts to model instances ---
            constructions = []
            for construction_data in property_data.constructions:
                if isinstance(construction_data, dict):
                    construction_data = schemas.ConstructionCreate(**construction_data)
                construction_type = db.query(models.ConstructionType).filter_by(name=construction_data.constructionType).first()
                if not construction_type:
                    raise HTTPException(status_code=400, detail=f"Invalid construction type: {construction_data.constructionType}")
                # Calculate capitalValue and houseTax as per user instruction
                
                #for capital_value calculation
                AreaInMeter = construction_data.length * construction_data.width * 0.092903
                AnnualLandValueRate = 1000
                ConstructionRateAsPerConstruction = construction_type.bandhmastache_dar
                depreciationRate = calculate_depreciation_rate(construction_data.constructionYear, construction_type.name)
                usageBasedBuildingWeightageFactor = 1
                

                capital_value = (( AreaInMeter * AnnualLandValueRate ) + ( AreaInMeter * ConstructionRateAsPerConstruction * depreciationRate)) * usageBasedBuildingWeightageFactor
                house_tax = round((getattr(construction_type, 'rate', 0) / 1000) * capital_value)
                new_construction = models.Construction(
                    construction_type_id=construction_type.id,
                    length=construction_data.length,
                    width=construction_data.width,
                    constructionYear=construction_data.constructionYear,
                    floor=construction_data.floor,
                    bharank=construction_data.bharank,
                    capitalValue=capital_value,
                    houseTax=house_tax,
                )
                constructions.append(new_construction)
            # --- END FIX ---

            # --- ADDITION: Handle vacant land construction if needed ---
            vacant_land_type = property_data.vacantLandType
            print("vacant " + str(vacant_land_type))
            has_khali_jaga = False
            for c in constructions:
                ctype = db.query(models.ConstructionType).filter_by(id=c.construction_type_id).first()
                if ctype and ctype.name.strip().startswith("खाली जागा"):
                    has_khali_jaga = True
                    break
            if not has_khali_jaga:
                # Use totalAreaSqFt if present, otherwise fallback to totalArea, otherwise calculate from lengths
                total_area = getattr(property_data, 'totalAreaSqFt', None)
                if total_area is None or total_area == 0:
                    total_area = getattr(property_data, 'totalArea', None)
                if total_area is None or total_area == 0:
                    east = getattr(property_data, 'eastLength', 0) or 0
                    west = getattr(property_data, 'westLength', 0) or 0
                    north = getattr(property_data, 'northLength', 0) or 0
                    south = getattr(property_data, 'southLength', 0) or 0
                    try:
                        avg_length = (float(east) + float(west)) / 2 if east or west else 0
                        avg_width = (float(north) + float(south)) / 2 if north or south else 0
                        total_area = avg_length * avg_width if avg_length and avg_width else 0
                    except (TypeError, ValueError):
                        total_area = 0
                try:
                    total_area = float(total_area)
                except (TypeError, ValueError):
                    total_area = 0

                # Sum all construction areas, converting to float
                used_area = sum(
                    float(getattr(c, 'length', 0) or 0) * float(getattr(c, 'width', 0) or 0)
                    for c in constructions
                )
                remaining_area = total_area - used_area
                print("remaining_area:", remaining_area)
                if remaining_area > 0:
                    print("greater")
                    vacant_type_obj = db.query(models.ConstructionType).filter(models.ConstructionType.name == vacant_land_type).first()
                    if vacant_type_obj:
                       
                        length = remaining_area
                        width = 1
                        constructionYear = str(datetime.now().year)
                        floor = "तळमजला"
                        bharank = "औद्योगिक"
                        AreaInMeter = length * width * 0.092903
                        AnnualLandValueRate = 1000
                        ConstructionRateAsPerConstruction = vacant_type_obj.bandhmastache_dar
                        depreciationRate = calculate_depreciation_rate(constructionYear, vacant_type_obj.name)
                        usageBasedBuildingWeightageFactor = 1
                        capital_value = (( AreaInMeter * AnnualLandValueRate ) + ( AreaInMeter * ConstructionRateAsPerConstruction * depreciationRate)) * usageBasedBuildingWeightageFactor
                        house_tax = round((getattr(vacant_type_obj, 'rate', 0) / 1000) * capital_value)
                        new_vacant_land = models.Construction(
                            construction_type_id=vacant_type_obj.id,
                            length=length,
                            width=width,
                            constructionYear=constructionYear,
                            floor=floor,
                            bharank=bharank,
                            capitalValue=capital_value,
                            houseTax=house_tax,
                        )
                        constructions.append(new_vacant_land)
            # --- END ADDITION ---

            property_dict = property_data.dict(exclude={"owners", "constructions"})
            db_property = models.Property(**property_dict, owners=owners, constructions=constructions)
            db_property.created_at = datetime.now()
            db.add(db_property)
            # Only set boolean fields and toilet (not calculated tax fields)
            db_property.divaArogyaKar = bool(property_data.divaArogyaKar)
            db_property.safaiKar = bool(property_data.safaiKar)
            db_property.shauchalayKar = bool(property_data.shauchalayKar)
            db_property.toilet = property_data.toilet if property_data.toilet is not None else ''
            db.flush()
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
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save property and owners: " + str(e))

@router.get("/property_list/", response_model=list[schemas.PropertyList])
def get_property_list(village: str, db: Session = Depends(database.get_db)):
    # Find the village by name
    village_obj = db.query(models.Village).filter(models.Village.name == village).first()
    if not village_obj:
        return []
    properties = db.query(models.Property).filter(models.Property.village_id == village_obj.id).all()
    result = []
    for p in properties:
        if p.owners:
            owner_name = ','.join([f"{i+1}.{o.name}" for i, o in enumerate(p.owners)])
        else:
            owner_name = "N/A"
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
def update_namuna8_entry(anu_kramank: int, property_data: schemas.PropertyUpdate, db: Session = Depends(database.get_db)):
    db_property = db.query(models.Property).filter(models.Property.anuKramank == anu_kramank).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    property_update_data = property_data.dict(exclude={'owners', 'constructions'})
    for key, value in property_update_data.items():
        setattr(db_property, key, value)
    db_property.updated_at = datetime.now()

    if property_data.owners:
        new_owners = []
        for owner_data in property_data.owners:
            # Accept dict or Pydantic model
            if isinstance(owner_data, dict):
                owner_data = schemas.OwnerUpdate(**owner_data)
            owner_id = getattr(owner_data, 'id', None)
            owner = None
            if owner_id is not None:
                # Ensure owner_id is an integer for matching
                if isinstance(owner_id, str) and owner_id.isdigit():
                    owner_id = int(owner_id)
                elif isinstance(owner_id, float):
                    owner_id = int(owner_id)
                owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
            if owner:
                # Update existing owner fields
                owner.name = owner_data.name
                if owner_data.aadhaarNumber is not None:
                    owner.aadhaarNumber = owner_data.aadhaarNumber
                if owner_data.mobileNumber is not None:
                    owner.mobileNumber = owner_data.mobileNumber
                if owner_data.wifeName is not None:
                    owner.wifeName = owner_data.wifeName
                if owner_data.occupantName is not None:
                    owner.occupantName = owner_data.occupantName
                owner_photo_val = getattr(owner_data, 'ownerPhoto', None)
                if owner_photo_val is not None and isinstance(owner_photo_val, str) and owner_photo_val != '':
                    owner.ownerPhoto = owner_photo_val
                if owner_data.village_id is not None:
                    owner.village_id = owner_data.village_id
                owner.updated_at = datetime.now()
                db.commit()
                new_owners.append(owner)
            else:
                # Always create new owner if id is null or does not match
                owner = models.Owner(
                    name=owner_data.name,
                    aadhaarNumber=owner_data.aadhaarNumber,
                    mobileNumber=owner_data.mobileNumber,
                    wifeName=owner_data.wifeName,
                    occupantName=owner_data.occupantName,
                    ownerPhoto=getattr(owner_data, 'ownerPhoto', None) if getattr(owner_data, 'ownerPhoto', None) is not None and isinstance(getattr(owner_data, 'ownerPhoto', None), str) and getattr(owner_data, 'ownerPhoto', None) != '' else None,
                    village_id=owner_data.village_id
                )
                db.add(owner)
                db.commit()
                db.refresh(owner)
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
            # Set capitalValue and houseTax as in create
            capital_value = 541133
            house_tax = round((getattr(construction_type, 'rate', 0) / 1000) * 541133)
            new_construction = models.Construction(
                construction_type_id=construction_type.id,
                length=construction_data.length,
                width=construction_data.width,
                constructionYear=construction_data.constructionYear,
                floor=construction_data.floor,
                bharank=construction_data.bharank,
                capitalValue=capital_value,
                houseTax=house_tax,
            )
            new_constructions.append(new_construction)
        db_property.constructions = new_constructions
    # --- END FIX ---

    db_property.divaArogyaKar = bool(property_data.divaArogyaKar)
    db_property.safaiKar = bool(property_data.safaiKar)
    db_property.shauchalayKar = bool(property_data.shauchalayKar)
    db_property.toilet = property_data.toilet if property_data.toilet is not None else ''

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
    # Prepare settings for tax and water calculations
    settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    water_settings = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == 'namuna8').first()
    water_slab_settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
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
    def get_water_facility_price(facility):
        if not facility:
            return 0
        if not water_settings or not water_slab_settings:
            return 0
        if facility == 'सामान्य पाणिकर':
            return getattr(water_settings, 'generalWater', 0)
        elif facility == 'घरगुती नळ':
            return getattr(water_settings, 'houseTax', 0)
        elif facility == 'व्यावसायिक नळ':
            return getattr(water_settings, 'commercialTax', 0)
        elif facility == 'कारस पात्र नसलेली इमारत':
            return getattr(water_settings, 'exemptRate', 0)
        elif facility == 'सामान्य पाणिकर १ ते ३०० ची फु.':
            return getattr(water_slab_settings, 'generalWaterUpto300', 0)
        elif facility == 'सामान्य पाणिकर ३०१ ते ७०० ची फु.':
            return getattr(water_slab_settings, 'generalWater301_700', 0)
        elif facility == 'सामान्य पाणिकर ७०० ची फु. वरील':
            return getattr(water_slab_settings, 'generalWaterAbove700', 0)
        return 0
    result = []
    for idx, p in enumerate(properties, start=1):
        owner_name = p.owners[0].name if p.owners else ""
        total_area = p.totalAreaSqFt or 0
        divaArogyaKar = bool(getattr(p, 'divaArogyaKar', False))
        result.append(schemas.BulkEditPropertyRow(
            serial_no=idx,
            malmattaKramank=p.malmattaKramank,
            ownerName=owner_name,
            occupant="स्वतः",  # Always 'self' for now
            gharKar=getattr(p, 'gharKar', 0),
            divaKar=get_tax_by_area(total_area, 'light') if not divaArogyaKar else 0,
            aarogyaKar=get_tax_by_area(total_area, 'health') if not divaArogyaKar else 0,
            sapanikar=get_water_facility_price(getattr(p, 'waterFacility1', None)),
            vpanikar=get_water_facility_price(getattr(p, 'waterFacility2', None)),
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
        if update.toilet is not None:
            prop.toilet = update.toilet
        if update.roofType is not None:
            prop.roofType = update.roofType
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
    aadhaarNumber: str = Body(None),
    mobileNumber: str = Body(...),
    village_id: int = Body(...),
    wifeName: str = Body(None),
    db: Session = Depends(database.get_db)
):
    # Check if owner with same aadhaarNumber exists, only if aadhaarNumber is provided
    if aadhaarNumber not in (None, ""):
        existing_owner = db.query(models.Owner).filter(models.Owner.aadhaarNumber == aadhaarNumber).first()
        if existing_owner:
            return {"detail": "Owner with this Aadhaar number already exists."}
    new_owner = models.Owner(
        name=name,
        aadhaarNumber=aadhaarNumber,
        mobileNumber=mobileNumber,
        wifeName=wifeName,
        village_id=village_id
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
        "village_id": new_owner.village_id
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
    # Calculate taxes and water charges on the fly
    settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    water_settings = db.query(models.Namuna8WaterTaxSettings).filter(models.Namuna8WaterTaxSettings.id == 'namuna8').first()
    water_slab_settings = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
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
    def get_water_facility_price(facility):
        if not facility:
            return 0
        if not water_settings or not water_slab_settings:
            return 0
        if facility == 'सामान्य पाणिकर':
            return getattr(water_settings, 'generalWater', 0)
        elif facility == 'घरगुती नळ':
            return getattr(water_settings, 'houseTax', 0)
        elif facility == 'व्यावसायिक नळ':
            return getattr(water_settings, 'commercialTax', 0)
        elif facility == 'कारस पात्र नसलेली इमारत':
            return getattr(water_settings, 'exemptRate', 0)
        elif facility == 'सामान्य पाणिकर १ ते ३०० ची फु.':
            return getattr(water_slab_settings, 'generalWaterUpto300', 0)
        elif facility == 'सामान्य पाणिकर ३०१ ते ७०० ची फु.':
            return getattr(water_slab_settings, 'generalWater301_700', 0)
        elif facility == 'सामान्य पाणिकर ७०० ची फु. वरील':
            return getattr(water_slab_settings, 'generalWaterAbove700', 0)
        return 0
    total_area = db_property.totalAreaSqFt or 0
    divaArogyaKar = bool(getattr(db_property, 'divaArogyaKar', False))
    safaiKar = bool(getattr(db_property, 'safaiKar', False))
    shauchalayKar = bool(getattr(db_property, 'shauchalayKar', False))
    property_dict = {
        **{k: getattr(db_property, k) for k in schemas.PropertyBase.__fields__.keys()},
        "owners": owners,
        "constructions": constructions,
        "divaKar": get_tax_by_area(total_area, 'light') if not divaArogyaKar else 0,
        "aarogyaKar": get_tax_by_area(total_area, 'health') if not divaArogyaKar else 0,
        "cleaningTax": get_tax_by_area(total_area, 'cleaning') if safaiKar else 0,
        "toiletTax": get_tax_by_area(total_area, 'bathroom') if shauchalayKar else 0,
        "sapanikar": get_water_facility_price(getattr(db_property, 'waterFacility1', None)),
        "vpanikar": get_water_facility_price(getattr(db_property, 'waterFacility2', None)),
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

@router.get("/settings/tax/waterslab/fields", response_model=dict)
def get_water_slab_fields(db: Session = Depends(database.get_db)):
    obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
    if not obj:
        return {"generalWaterUpto300": 0, "generalWater301_700": 0, "generalWaterAbove700": 0}
    return {
        "generalWaterUpto300": obj.generalWaterUpto300,
        "generalWater301_700": obj.generalWater301_700,
        "generalWaterAbove700": obj.generalWaterAbove700
    }

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
        # Update Namuna8SettingTax fields instead of Namuna8GeneralWaterTaxSlabSettings
        settingtax_obj = db.query(models.Namuna8SettingTax).filter(models.Namuna8SettingTax.id == 'namuna8').first()
        if settingtax_obj:
            if 'rateUpto300' in watertaxslab_data:
                settingtax_obj.generalWaterUpto300 = watertaxslab_data['rateUpto300']
            if 'rate301To700' in watertaxslab_data:
                settingtax_obj.generalWater301_700 = watertaxslab_data['rate301To700']
            if 'rateAbove700' in watertaxslab_data:
                settingtax_obj.generalWaterAbove700 = watertaxslab_data['rateAbove700']
            db.commit()
            db.refresh(settingtax_obj)
            result['watertaxslab'] = settingtax_obj
        else:
            # If not found, create with only these fields
            settingtax_obj = models.Namuna8SettingTax(
                id='namuna8',
                generalWaterUpto300=watertaxslab_data.get('rateUpto300', 0),
                generalWater301_700=watertaxslab_data.get('rate301To700', 0),
                generalWaterAbove700=watertaxslab_data.get('rateAbove700', 0)
            )
            db.add(settingtax_obj)
            db.commit()
            db.refresh(settingtax_obj)
            result['watertaxslab'] = settingtax_obj
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

@router.get("/owners_by_village/", response_model=List[schemas.Owner])
def get_owners_by_village(village_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Owner).filter(models.Owner.village_id == village_id).all()

@router.get("/properties_by_village/", response_model=List[schemas.PropertyRead])
def get_properties_by_village(village_id: int, db: Session = Depends(database.get_db)):
    properties = db.query(models.Property).filter(models.Property.village_id == village_id).all()
    return [build_property_response(p, db) for p in properties]

@router.get("/properties_by_owner/", response_model=List[schemas.PropertyRead])
def get_properties_by_owner(owner_id: int, db: Session = Depends(database.get_db)):
    owner = db.query(models.Owner).filter(models.Owner.id == owner_id).first()
    if not owner:
        return []
    return [build_property_response(p, db) for p in owner.properties]

@router.get("/properties/bulk", response_model=list[schemas.PropertyRead])
def get_properties_bulk(ids: str = Query(...), db: Session = Depends(database.get_db)):
    # ids is a comma-separated string of property IDs
    id_list = [int(i) for i in ids.split(",") if i.strip().isdigit()]
    properties = db.query(models.Property).filter(models.Property.anuKramank.in_(id_list)).all()
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
        prop.divaKar = get_tax_by_area(total_area, 'light') if not prop.divaArogyaKar else 0
        prop.aarogyaKar = get_tax_by_area(total_area, 'health') if not prop.divaArogyaKar else 0
        prop.cleaningTax = get_tax_by_area(total_area, 'cleaning') if prop.safaiKar else 0
        toilet_tax = get_tax_by_area(total_area, 'bathroom') if prop.shauchalayKar else 0.0
        prop.toiletTax = toilet_tax
    db.commit()
    return {"detail": "All property taxes recalculated and updated."}

@router.get("/all_properties/")
def get_all_properties(db: Session = Depends(database.get_db)):
    return db.query(models.Property).all()

@router.delete("/{anu_kramank}", status_code=200)
def delete_property(anu_kramank: int, db: Session = Depends(database.get_db)):
    prop = db.query(models.Property).filter(models.Property.anuKramank == anu_kramank).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    # Remove associations with owners (many-to-many)
    prop.owners = []
    db.commit()
    # Explicitly delete all constructions associated with this property
    for construction in list(prop.constructions):
        db.delete(construction)
    db.commit()
    # Delete the property
    db.delete(prop)
    db.commit()
    return {"message": f"Property {anu_kramank} deleted successfully."}
    