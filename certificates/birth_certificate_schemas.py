from pydantic import BaseModel
from typing import Optional
from datetime import date

class BirthCertificateBase(BaseModel):
    date: Optional[date]
    register_date: Optional[date]
    village: Optional[str]
    child_name: Optional[str]
    child_name_en: str
    gender: Optional[str]
    sex: Optional[str]
    panhera: Optional[str]
    birth_date: Optional[date]
    birth_place: Optional[str]
    mother_name: Optional[str]
    mother_name_en: str
    father_name: Optional[str]
    father_name_en: str
    address_at_birth: Optional[str]
    address_at_birth_en: str
    permanent_address: Optional[str]
    permanent_address_en: str
    remark: Optional[str]
    remark_en: str

class BirthCertificateCreate(BirthCertificateBase):
    pass

class BirthCertificateRead(BirthCertificateBase):
    id: int
    class Config:
        orm_mode = True 