from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from namuna8 import namuna8_model as models
from namuna8 import namuna8_schemas as schemas
from database import get_db
from datetime import datetime
from namuna8.calculations.naumuna8_calculations import calculate_depreciation_rate

router = APIRouter()

# Helper to calculate house tax
def calc_house_tax(rate):
    try:
        if rate is None:
            return 0
        capital_value = 541133
        return round((float(rate) / 1000) * capital_value)
    except Exception:
        return 0

@router.get("/property_record/{anuKramank}")
def get_property_record(anuKramank: int, db: Session = Depends(get_db)):
    prop = db.query(models.Property).filter(models.Property.anuKramank == anuKramank).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    owner_ids = [o.id for o in prop.owners]
    property_types = [c.construction_type.name for c in prop.constructions]
    property_description = ", ".join(property_types)
    # khaliJaga logic
    khali_jaga_types = [c for c in prop.constructions if c.construction_type.name.strip() == "खाली जागा"]
    khaliJaga = []
    if khali_jaga_types:
        for c in khali_jaga_types:
            # Find the rate for 'खाली जागा' from constructionType
            khali_jaga_rate = getattr(c.construction_type, 'rate', None)
            area_foot = (c.length or 0) * (c.width or 0)
            area_meter = round(area_foot * 0.092903, 2)
            khaliJaga.append({
                "constructiontype": c.construction_type.name,
                "length": c.length,
                "width": c.width,
                "year": datetime.now().year,
                "rate": khali_jaga_rate,
                "floor": c.floor,
                "usage": getattr(c, 'bharank', None),
                "capitalValue": 541133,
                "houseTax": round((getattr(c.construction_type, 'rate', 0) / 1000) * 541133),
                "usageBasedBuildingWeightageFactor": 1,
                "taxRates": getattr(c.construction_type, 'bandhmastache_dar', None),
                "totalkhalijagaareainfoot": area_foot,
                "totalkhalijagaareainmeters": area_meter
            })
    else:
        total_area = prop.totalAreaSqFt or 0
        used_area = sum((c.length or 0) * (c.width or 0) for c in prop.constructions)
        khali_area = max(total_area - used_area, 0)
        if khali_area > 0:
            # Find the rate for 'खाली जागा' from constructionType (if any)
            khali_jaga_rate = None
            for c in prop.constructions:
                if c.construction_type.name.strip().startswith("खाली जागा"):
                    khali_jaga_rate = getattr(c.construction_type, 'rate', None)
                    break
            area_foot = khali_area * 1
            area_meter = round(area_foot * 0.092903, 2)
            khaliJaga.append({
                "constructiontype": "खाली जागा",
                "length": khali_area,
                "width": 1,
                "year": datetime.now().year,
                "rate": khali_jaga_rate,
                "floor": None,
                "usage": None,
                "capitalValue": 541133,
                "houseTax": 0,
                "usageBasedBuildingWeightageFactor": 1,
                "taxRates": None,
                "totalkhalijagaareainfoot": area_foot,
                "totalkhalijagaareainmeters": area_meter
            })
    constructionType = [
        {
            "type": c.construction_type.name,
            "length": c.length,
            "width": c.width,
            "year": c.constructionYear,
            "rate": getattr(c.construction_type, 'rate', None),
            "floor": c.floor,
            "usage": getattr(c, 'bharank', None),
            "capitalValue": 541133,
            "houseTax": round((getattr(c.construction_type, 'rate', 0) / 1000) * 541133),
            "depreciation_rate": calculate_depreciation_rate(c.constructionYear, c.construction_type.name),
            "usageBasedBuildingWeightageFactor": 1,
            "taxRates": getattr(c.construction_type, 'bandhmastache_dar', None)
        }
        for c in prop.constructions
    ]
    owner = prop.owners[0] if prop.owners else None
    # Fetch Namuna8SettingTax row
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
    total_area = prop.totalAreaSqFt or 0
    response = {
        "id": str(prop.anuKramank),
        "srNo": prop.anuKramank,
        "propertyNumber": str(prop.malmattaKramank),
        "propertyDescription": property_description,
        "gramPanchayat": prop.village.name if hasattr(prop, 'village') and prop.village else None,
        "village": prop.village.name if hasattr(prop, 'village') and prop.village else None,
        "taluka": None,
        "jilha": None,
        "yearFrom": 2024,
        "yearTo": 2027,
        "photoURL": None,
        "QRcodeURL": None,
        "total_arearinfoot": prop.totalAreaSqFt,
        "totalareainmeters": round((prop.totalAreaSqFt or 0) * 0.092903, 2),
        "occupantName": owner.occupantName if owner else None,
        "aadharNumber": owner.aadhaarNumber if owner else None,
        "ownerName": owner.name if owner else None,
        "roadName": prop.streetName,
        "cityWardGatNumber": prop.citySurveyOrGatNumber,
        "areaEast": prop.eastLength,
        "areaWest": prop.westLength,
        "areaNorth": prop.northLength,
        "areaSouth": prop.southLength,
        "totalArea": prop.totalAreaSqFt,
        "boundaryEast": prop.eastBoundary,
        "boundaryWest": prop.westBoundary,
        "boundaryNorth": prop.northBoundary,
        "boundarySouth": prop.southBoundary,
        "removeLightHealthTax": prop.divaArogyaKar,
        "applyCleaningTax": prop.safaiKar,
        "applyToiletTax": prop.shauchalayKar,
        "taxNotApplicable": prop.karLaguNahi,
        "khaliJaga": khaliJaga,
        "constructionType": constructionType,
        "waterFacility1": prop.waterFacility1,
        "waterFacility2": prop.waterFacility2,
        "toilet": str(prop.toilet) if prop.toilet is not None else "",
        "house": prop.roofType,
        "totalCapitalValue": 0,
        "totalHouseTax": int(getattr(prop, 'gharKar', 0)),
        "housingUnit": prop.areaUnit,
        "lightingTax": get_tax_by_area(total_area, 'light') if prop.divaArogyaKar else 0,
        "healthTax": get_tax_by_area(total_area, 'health') if prop.divaArogyaKar else 0,
        "waterTax": 0,  # Not specified in Namuna8SettingTax
        "cleaningTax": get_tax_by_area(total_area, 'cleaning') if prop.safaiKar else 0,
        "toiletTax": get_tax_by_area(total_area, 'bathroom') if prop.shauchalayKar else 0,
        "totaltax": 0,
        "userId": owner_ids,
        "villageId": str(prop.village_id),
        "creationAt": datetime.now(),
        "updationAt": datetime.now(),
       
    }
    return response 