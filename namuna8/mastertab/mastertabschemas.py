from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GeneralSettingBase(BaseModel):
    typingLanguage: Optional[str] = None
    capitalFormula1: Optional[bool] = None
    capitalFormula2: Optional[bool] = None
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None

class GeneralSettingCreate(GeneralSettingBase):
    id: Optional[str] = None

class GeneralSettingRead(GeneralSettingBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True

class BuildingUsageWeightageBase(BaseModel):
    serial_number: int
    building_usage: str
    weightage: float
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None

class BuildingUsageWeightageCreate(BuildingUsageWeightageBase):
    pass

class BuildingUsageWeightageRead(BuildingUsageWeightageBase):
    id: int
    class Config:
        orm_mode = True

class NewYojnaBase(BaseModel):
    yojnaName: str
    yojnaDescription: Optional[str] = None
    consession: Optional[str] = None
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None

class NewYojnaCreate(NewYojnaBase):
    id: int

class NewYojnaRead(NewYojnaBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True 