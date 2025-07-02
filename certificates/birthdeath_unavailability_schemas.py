from pydantic import BaseModel
from typing import Optional
from datetime import date

class BirthDeathUnavailabilityCertificateBase(BaseModel):
    register_date: Optional[date]
    village: Optional[str]
    village_en: Optional[str]
    applicant_name: Optional[str]
    applicant_name_en: Optional[str]
    adhar_number: Optional[str]
    adhar_number_en: Optional[str]
    certificate_name: Optional[str]
    certificate_name_en: Optional[str]
    subject: Optional[str]
    subject_en: Optional[str]

class BirthDeathUnavailabilityCertificateCreate(BirthDeathUnavailabilityCertificateBase):
    pass

class BirthDeathUnavailabilityCertificateRead(BirthDeathUnavailabilityCertificateBase):
    id: int
    class Config:
        orm_mode = True 