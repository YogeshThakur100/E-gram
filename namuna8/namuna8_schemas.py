from typing import List, Optional
from pydantic import BaseModel

# --- Owner Schemas ---
class OwnerBase(BaseModel):
    name: str
    aadhaarNumber: Optional[str] = None
    mobileNumber: Optional[str] = None
    wifeName: Optional[str] = None
    occupantName: Optional[str] = None
    # No streetName or city fields here
    ownerPhoto: Optional[str] = None
    streetName: Optional[str] = None
    citySurveyOrGatNumber: Optional[str] = None

class OwnerCreate(OwnerBase):
    pass

class Owner(OwnerBase):
    id: int

    class Config:
        from_attributes = True

# --- Construction Schemas ---
class ConstructionBase(BaseModel):
    constructionType: str
    length: float
    width: float
    constructionYear: str
    floor: str
    usage: str
    bharank: Optional[str] = None

class ConstructionCreate(ConstructionBase):
    pass

class Construction(ConstructionBase):
    id: int
    class Config:
        from_attributes = True

# --- Property Schemas ---
class PropertyBase(BaseModel):
    villageOrMoholla: str
    anuKramank: int
    malmattaKramank: int
    streetName: Optional[str] = None
    citySurveyOrGatNumber: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None
    totalAreaSqFt: Optional[float] = None
    eastBoundary: Optional[str] = None
    westBoundary: Optional[str] = None
    northBoundary: Optional[str] = None
    southBoundary: Optional[str] = None
    divaArogyaKar: Optional[bool] = False
    safaiKar: Optional[bool] = False
    shauchalayKar: Optional[bool] = False
    karLaguNahi: Optional[bool] = False
    vacantLandType: Optional[str] = None
    waterFacility1: Optional[str] = None
    waterFacility2: Optional[str] = None
    toilet: Optional[str] = None
    roofType: Optional[str] = None
    eastBoundary2: Optional[str] = None
    westBoundary2: Optional[str] = None
    northBoundary2: Optional[str] = None
    southBoundary2: Optional[str] = None
    eastLength: Optional[float] = None
    westLength: Optional[float] = None
    northLength: Optional[float] = None
    southLength: Optional[float] = None
    areaUnit: Optional[str] = None

class PropertyCreate(PropertyBase):
    owners: List[OwnerCreate]
    constructions: List[ConstructionCreate]

class PropertyRead(PropertyBase):
    owners: List[Owner] = []
    constructions: List[Construction] = []

    class Config:
        from_attributes = True

# --- Schema for the property list on the side ---
class PropertyList(BaseModel):
    malmattaKramank: int
    ownerName: str
    anuKramank: int

class BulkEditPropertyRow(BaseModel):
    serial_no: int
    malmattaKramank: int
    ownerName: str
    occupant: str  # always 'स्वतः' for now
    gharKar: float
    divaKar: float
    aarogyaKar: float
    sapanikar: float
    vpanikar: float

    class Config:
        orm_mode = True

class BulkEditUpdateRequest(BaseModel):
    property_ids: list[int]
    waterFacility1: Optional[str] = None
    waterFacility2: Optional[str] = None
    toilet: Optional[str] = None
    house: Optional[str] = None
    divaArogyaKar: Optional[bool] = None
    safaiKar: Optional[bool] = None
    shauchalayKar: Optional[bool] = None
    karLaguNahi: Optional[bool] = None
    # Add more fields as needed

class PropertyReportDTO(BaseModel):
    sr_no: int
    village_info: Optional[str] = None
    owner_name: Optional[str] = None
    occupant_name: Optional[str] = None
    property_description: Optional[str] = None
    property_numbers: Optional[str] = None
    dimension: Optional[str] = None
    area_sqft_sqm: Optional[str] = None
    rate_per_sqm: Optional[str] = None
    depreciation_info: Optional[str] = None
    usage_factor: Optional[str] = None
    tax_rate_paise: Optional[str] = None
    capital_value: Optional[str] = None
    tax_percentage: Optional[str] = None
    tax_amount_rupees: Optional[str] = None
    land_tax: Optional[str] = None
    building_tax: Optional[str] = None
    construction_tax: Optional[str] = None
    house_tax: Optional[str] = None
    light_tax: Optional[str] = None
    total_tax: Optional[str] = None