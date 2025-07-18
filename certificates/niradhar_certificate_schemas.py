from pydantic import BaseModel, constr, validator
from datetime import date

class NiradharCertificateBase(BaseModel):
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

class NiradharCertificateCreate(NiradharCertificateBase):
    pass

class NiradharCertificateRead(NiradharCertificateBase):
    id: int
    barcode: str | None = None
    barcode_url: str | None = None
    gramPanchayat: str | None = None
    taluka: str | None = None
    jilha: str | None = None
    class Config:
        from_attributes = True 