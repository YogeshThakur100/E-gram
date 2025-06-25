from pydantic import BaseModel, constr, validator
from typing import Annotated
from datetime import date

class ToiletCertificateBase(BaseModel):
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

class ToiletCertificateCreate(ToiletCertificateBase):
    pass

class ToiletCertificateRead(ToiletCertificateBase):
    id: int
    class Config:
        orm_mode = True 