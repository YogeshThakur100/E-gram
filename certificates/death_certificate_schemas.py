from pydantic import BaseModel
from typing import Optional
from datetime import date

class DeathCertificateBase(BaseModel):
    date: Optional[date]
    register_date: Optional[date]
    village: Optional[str]
    deceased_name: Optional[str]
    sex: Optional[str]
    death_date: Optional[date]
    place_of_death: Optional[str]
    mother_name: Optional[str]
    father_name: Optional[str]
    address_at_death: Optional[str]
    permanent_address: Optional[str]
    remark: Optional[str]
    deceased_name_en: Optional[str]
    place_of_death_en: Optional[str]
    mother_name_en: Optional[str]
    father_name_en: Optional[str]
    address_at_death_en: Optional[str]
    permanent_address_en: Optional[str]
    remark_en: Optional[str]

class DeathCertificateCreate(DeathCertificateBase):
    pass

class DeathCertificateRead(DeathCertificateBase):
    id: int
    class Config:
        orm_mode = True 