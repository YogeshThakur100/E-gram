from pydantic import BaseModel
from typing import Optional

class Namuna9YearSetupBase(BaseModel):
    village: str
    year: str
    data_source: str
    notes: Optional[str] = None
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None
    # Add more fields as needed for section 2/3
    # previous_year: Optional[str] = None
    # shakti_option: Optional[str] = None

class Namuna9YearSetupCreate(Namuna9YearSetupBase):
    pass

class Namuna9YearSetupRead(Namuna9YearSetupBase):
    id: int
    class Config:
        orm_mode = True

class Namuna9CarryForward(BaseModel):
    village: str
    from_year: str
    to_year: str
    carry_forward_option: str # e.g., "मागील एकूण चे" ~

class Namuna9SettingsBase(BaseModel):
    penalty_percentage: int
    notice_fee: int
    warrant_fee: int
    notes: Optional[str] = None
    keep_namuna9_date: bool = False
    keep_notice_date: bool = False
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None

class Namuna9SettingsCreate(Namuna9SettingsBase):
    pass

class Namuna9SettingsRead(Namuna9SettingsBase):
    id: int
    class Config:
        orm_mode = True
class Namuna9SettingsUpdate(BaseModel):
    penalty_percentage: Optional[int] = None
    notice_fee: Optional[int] = None
    warrant_fee: Optional[int] = None
    notes: Optional[str] = None
    keep_namuna9_date: Optional[bool] = None
    keep_notice_date: Optional[bool] = None
    district_id: Optional[int] = None
    taluka_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None