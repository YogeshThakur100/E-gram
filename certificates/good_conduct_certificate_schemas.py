from pydantic import BaseModel, constr, validator
from datetime import date
from typing import Optional

class GoodConductCertificateBase(BaseModel):
    registration_date: date
    village: str
    village_en: str
    applicant_name: str
    applicant_name_en: str
    adhar_number: constr(min_length=4)
    adhar_number_en: constr(min_length=4)

    @validator('adhar_number', 'adhar_number_en')
    def must_be_digits(cls, v):
        if not v.isdigit():
            raise ValueError('Aadhaar number must be digits only')
        return v

class GoodConductCertificateCreate(GoodConductCertificateBase):
    pass

class GoodConductCertificateRead(GoodConductCertificateBase):
    id: int
    image_url: Optional[str] = None
    class Config:
        orm_mode = True 