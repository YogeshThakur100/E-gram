from pydantic import BaseModel
from typing import Optional
from datetime import date

class ResidentCertificateBase(BaseModel):
    dispatch_no: Optional[str]
    date: Optional[date]
    village: Optional[str]
    village_en: Optional[str]
    applicant_name: Optional[str]
    applicant_name_en: Optional[str]
    adhar_no: Optional[str]
    adhar_no_en: Optional[str]
    image_url: Optional[str]

class ResidentCertificateCreate(ResidentCertificateBase):
    pass

class ResidentCertificateRead(ResidentCertificateBase):
    id: int
    class Config:
        orm_mode = True 