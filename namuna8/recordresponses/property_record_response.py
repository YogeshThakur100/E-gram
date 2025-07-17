from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from namuna8 import namuna8_model as models
from namuna8 import namuna8_schemas as schemas
from database import get_db
from datetime import datetime
from namuna8.calculations.naumuna8_calculations import calculate_depreciation_rate
import os
backend_url = os.environ.get('BACKEND_URL', 'http://localhost:8000')

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
            khali_jaga_rate = getattr(c.construction_type, 'rate', 0)
            bandhmastache_dar = getattr(c.construction_type, 'bandhmastache_dar', 0)
            area_foot = (c.length or 0) * (c.width or 0)
            area_meter = round(area_foot * 0.092903, 2)
            khaliJaga.append({
                "constructiontype": c.construction_type.name,
                "length": c.length,
                "width": c.width,
                "year": datetime.now().year,
                "rate": bandhmastache_dar,
                "floor": c.floor,
                "usage": getattr(c, 'bharank', None),
                "capitalValue": c.capitalValue,
                "houseTax": c.houseTax,
                "usageBasedBuildingWeightageFactor": 1,
                "taxRates": khali_jaga_rate,
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
            bandhmastache_dar = None
            khali_jaga_construction = None
            for c in prop.constructions:
                if c.construction_type.name.strip() == "खाली जागा":
                    khali_jaga_rate = getattr(c.construction_type, 'rate', 0)
                    bandhmastache_dar = getattr(c.construction_type, 'bandhmastache_dar', 0)
                    khali_jaga_construction = c
                    break
            area_foot = khali_area * 1
            area_meter = round(area_foot * 0.092903, 2)
            khaliJaga.append({
                "constructiontype": "खाली जागा",
                "length": khali_area,
                "width": 1,
                "year": datetime.now().year,
                "rate": bandhmastache_dar,
                "floor": None,
                "usage": None,
                "capitalValue": khali_jaga_construction.capitalValue if khali_jaga_construction else None,
                "houseTax": khali_jaga_construction.houseTax if khali_jaga_construction else None,
                "usageBasedBuildingWeightageFactor": 1,
                "taxRates": khali_jaga_rate,
                "totalkhalijagaareainfoot": area_foot,
                "totalkhalijagaareainmeters": area_meter
            })
    constructionType = [
        {
            "type": c.construction_type.name,
            "length": c.length,
            "width": c.width,
            "year": c.constructionYear,
            "rate": getattr(c.construction_type, 'bandhmastache_dar', 0),
            "floor": c.floor,
            "usage": getattr(c, 'bharank', None),
            "capitalValue": c.capitalValue,
            "houseTax": c.houseTax,
            "depreciation_rate": calculate_depreciation_rate(c.constructionYear, c.construction_type.name),
            "usageBasedBuildingWeightageFactor": 1,
            "taxRates": getattr(c.construction_type, 'rate', 0),
        }
        for c in prop.constructions
    ]
    owner = prop.owners[0] if prop.owners else None
    # Find the first owner with a non-null ownerPhoto
    photo_url = None
    for o in prop.owners:
        if getattr(o, 'ownerPhoto', None):
            photo_url = f"{backend_url}/{o.ownerPhoto.replace(os.sep, '/')}"
            break
    # Fetch Namuna8SettingTax row
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
        # Accept both spellings for 'सामान्य पाणिकर' and 'सामान्य पाणीकर'
        if facility in ['सामान्य पाणिकर', 'सामान्य पाणीकर']:
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
    total_area = prop.totalAreaSqFt or 0
    # Calculate totalHouseTax as the sum of all houseTax in constructions (excluding 'खाली जागा')
    total_house_tax = sum([
        c.houseTax or 0
        for c in prop.constructions
        if not getattr(c.construction_type, 'name', '').strip().startswith('खाली जागा')
    ])
    
    # Calculate total capital value (excluding khali jagas)
    total_capital_value = sum([c.capitalValue or 0 for c in prop.constructions if not c.construction_type.name.strip().startswith("खाली जागा")])
    
    # Calculate total construction area in foot and meter (excluding khali jagas)
    total_construction_area_foot = sum([(c.length or 0) * (c.width or 0) for c in prop.constructions if not c.construction_type.name.strip().startswith("खाली जागा")])
    total_construction_area_meter = round(total_construction_area_foot * 0.092903, 2)
    
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
        "photoURL": photo_url,
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
        "totalCapitalValue": int(total_capital_value),
        "totalHouseTax": int(total_house_tax),
        "totalconstructionareainfoot": int(total_construction_area_foot),
        "totalconstructionareainmeter": total_construction_area_meter,
        "housingUnit": prop.areaUnit,
        "lightingTax": get_tax_by_area(total_area, 'light') if not prop.divaArogyaKar else 0,
        "healthTax": get_tax_by_area(total_area, 'health') if not prop.divaArogyaKar else 0,
        "waterTax": 0,  # Not specified in Namuna8SettingTax
        "cleaningTax": get_tax_by_area(total_area, 'cleaning') if prop.safaiKar else 0,
        "toiletTax": get_tax_by_area(total_area, 'bathroom') if prop.shauchalayKar else 0,
        "sapanikar": get_water_facility_price(prop.waterFacility1),
        "vpanikar": get_water_facility_price(prop.waterFacility2),
        "totaltax": 0,
        "userId": owner_ids,
        "villageId": str(prop.village_id),
        "creationAt": datetime.now(),
        "updationAt": datetime.now(),
       
    }
    # Calculate total tax as sum of houseTax in all constructions (excluding 'खाली जागा') plus lightingTax, healthTax, toiletTax, cleaningTax, sapanikar, and vpanikar
    house_tax_sum = sum([
        c.houseTax or 0
        for c in prop.constructions
        if not getattr(c.construction_type, 'name', '').strip().startswith('खाली जागा')
    ])
    totaltax = (
        house_tax_sum +
        response.get('lightingTax', 0) +
        response.get('healthTax', 0) +
        response.get('toiletTax', 0) +
        response.get('cleaningTax', 0) +
        response.get('sapanikar', 0) +
        response.get('vpanikar', 0)
    )
    response['totaltax'] = totaltax
    # Fetch Namuna8SettingChecklist row
    checklist = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == 'namuna8').first()
    checklist_fields = {}
    if checklist:
        checklist_dict = checklist.__dict__
        checklist_fields = {k: v for k, v in checklist_dict.items() if k not in ('id', 'createdAt', 'updatedAt', 'roundupArea', '_sa_instance_state')}
    # Add checklist fields at the end
    response.update(checklist_fields)
    # Set QRcodeURL if QR code exists (single property)
    qr_path = os.path.join("uploaded_images", "qrcode", str(prop.anuKramank), "qrcode.png")
    if os.path.exists(qr_path):
        response["QRcodeURL"] = f"{backend_url}/namuna8/property_qrcode/{prop.anuKramank}"
    else:
        response["QRcodeURL"] = None
    return response 

@router.get("/property_records_by_village/{village_id}")
def get_property_records_by_village(village_id: int, db: Session = Depends(get_db)):
    properties = db.query(models.Property).filter(models.Property.village_id == village_id).all()
    results = []
    # Fetch Namuna8SettingChecklist row only once
    checklist = db.query(models.Namuna8SettingChecklist).filter(models.Namuna8SettingChecklist.id == 'namuna8').first()
    checklist_fields = {}
    if checklist:
        checklist_dict = checklist.__dict__
        checklist_fields = {k: v for k, v in checklist_dict.items() if k not in ('id', 'createdAt', 'updatedAt', 'roundupArea', '_sa_instance_state')}
    for prop in properties:
        owner_ids = [o.id for o in prop.owners]
        property_types = [c.construction_type.name for c in prop.constructions]
        property_description = ", ".join(property_types)
        khali_jaga_types = [c for c in prop.constructions if c.construction_type.name.strip() == "खाली जागा"]
        khaliJaga = []
        if khali_jaga_types:
            for c in khali_jaga_types:
                khali_jaga_rate = getattr(c.construction_type, 'rate', 0)
                bandhmastache_dar = getattr(c.construction_type, 'bandhmastache_dar', 0)
                area_foot = (c.length or 0) * (c.width or 0)
                area_meter = round(area_foot * 0.092903, 2)
                khaliJaga.append({
                    "constructiontype": c.construction_type.name,
                    "length": c.length,
                    "width": c.width,
                    "year": datetime.now().year,
                    "rate": bandhmastache_dar,
                    "floor": c.floor,
                    "usage": getattr(c, 'bharank', None),
                    "capitalValue": c.capitalValue,
                    "houseTax": c.houseTax,
                    "usageBasedBuildingWeightageFactor": 1,
                    "taxRates": khali_jaga_rate,
                    "totalkhalijagaareainfoot": area_foot,
                    "totalkhalijagaareainmeters": area_meter
                })
        else:
            total_area = prop.totalAreaSqFt or 0
            used_area = sum((c.length or 0) * (c.width or 0) for c in prop.constructions)
            khali_area = max(total_area - used_area, 0)
            if khali_area > 0:
                khali_jaga_rate = None
                bandhmastache_dar = None
                khali_jaga_construction = None
                for c in prop.constructions:
                    if c.construction_type.name.strip() == "खाली जागा":
                        khali_jaga_rate = getattr(c.construction_type, 'rate', 0)
                        bandhmastache_dar = getattr(c.construction_type, 'bandhmastache_dar', 0)
                        khali_jaga_construction = c
                        break
                area_foot = khali_area * 1
                area_meter = round(area_foot * 0.092903, 2)
                khaliJaga.append({
                    "constructiontype": "खाली जागा",
                    "length": khali_area,
                    "width": 1,
                    "year": datetime.now().year,
                    "rate": bandhmastache_dar,
                    "floor": None,
                    "usage": None,
                    "capitalValue": khali_jaga_construction.capitalValue if khali_jaga_construction else None,
                    "houseTax": khali_jaga_construction.houseTax if khali_jaga_construction else None,
                    "usageBasedBuildingWeightageFactor": 1,
                    "taxRates": khali_jaga_rate,
                    "totalkhalijagaareainfoot": area_foot,
                    "totalkhalijagaareainmeters": area_meter
                })
        constructionType = [
            {
                "type": c.construction_type.name,
                "length": c.length,
                "width": c.width,
                "year": c.constructionYear,
                "rate": getattr(c.construction_type, 'bandhmastache_dar', 0),
                "floor": c.floor,
                "usage": getattr(c, 'bharank', None),
                "capitalValue": c.capitalValue,
                "houseTax": c.houseTax,
                "depreciation_rate": calculate_depreciation_rate(c.constructionYear, c.construction_type.name),
                "usageBasedBuildingWeightageFactor": 1,
                "taxRates": getattr(c.construction_type, 'rate', 0),
            }
            for c in prop.constructions
        ]
        owner = prop.owners[0] if prop.owners else None
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
        total_area = prop.totalAreaSqFt or 0
        # Calculate totalHouseTax as the sum of all houseTax in constructions (excluding 'खाली जागा')
        total_house_tax = sum([
            c.houseTax or 0
            for c in prop.constructions
            if not getattr(c.construction_type, 'name', '').strip().startswith('खाली जागा')
        ])
        total_capital_value = sum([c.capitalValue or 0 for c in prop.constructions if not c.construction_type.name.strip().startswith("खाली जागा")])
        total_construction_area_foot = sum([(c.length or 0) * (c.width or 0) for c in prop.constructions if not c.construction_type.name.strip().startswith("खाली जागा")])
        total_construction_area_meter = round(total_construction_area_foot * 0.092903, 2)
        response = {
            "id": str(prop.anuKramank),
            "anuKramank": prop.anuKramank,
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
            "totalCapitalValue": int(total_capital_value),
            "totalHouseTax": int(total_house_tax),
            "totalconstructionareainfoot": int(total_construction_area_foot),
            "totalconstructionareainmeter": total_construction_area_meter,
            "housingUnit": prop.areaUnit,
            "lightingTax": get_tax_by_area(total_area, 'light') if not prop.divaArogyaKar else 0,
            "healthTax": get_tax_by_area(total_area, 'health') if not prop.divaArogyaKar else 0,
            "waterTax": 0,
            "cleaningTax": get_tax_by_area(total_area, 'cleaning') if prop.safaiKar else 0,
            "toiletTax": get_tax_by_area(total_area, 'bathroom') if prop.shauchalayKar else 0,
            "sapanikar": get_water_facility_price(prop.waterFacility1),
            "vpanikar": get_water_facility_price(prop.waterFacility2),
            "totaltax": 0,
        }
        # Calculate total tax as sum of houseTax in all constructions (excluding 'खाली जागा') plus lightingTax, healthTax, toiletTax, cleaningTax, sapanikar, and vpanikar
        house_tax_sum = sum([
            c.houseTax or 0
            for c in prop.constructions
            if not getattr(c.construction_type, 'name', '').strip().startswith('खाली जागा')
        ])
        totaltax = (
            house_tax_sum +
            response.get('lightingTax', 0) +
            response.get('healthTax', 0) +
            response.get('toiletTax', 0) +
            response.get('cleaningTax', 0) +
            response.get('sapanikar', 0) +
            response.get('vpanikar', 0)
        )
        response['totaltax'] = totaltax
        # Find the first owner with a non-null ownerPhoto
        photo_url = None
        for o in prop.owners:
            if getattr(o, 'ownerPhoto', None):
                photo_url = f"{backend_url}/{o.ownerPhoto.replace(os.sep, '/')}"
                break
        response["photoURL"] = photo_url
        # Set QRcodeURL if QR code exists (bulk)
        qr_path = os.path.join("uploaded_images", "qrcode", str(prop.anuKramank), "qrcode.png")
        if os.path.exists(qr_path):
            response["QRcodeURL"] = f"{backend_url}/namuna8/property_qrcode/{prop.anuKramank}"
        else:
            response["QRcodeURL"] = None
        # Add checklist fields to the response
        response.update(checklist_fields)
        results.append(response)
    return results 