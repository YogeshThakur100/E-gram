from pydantic import BaseModel
from typing import Optional
from datetime import date

class NoArrearsCertificateBase(BaseModel):
    registration_date: date
    village: Optional[str] = None
    village_en: Optional[str] = None
    applicant_name: Optional[str] = None
    applicant_name_en: Optional[str] = None
    adhar_number: Optional[str] = None
    adhar_number_en: Optional[str] = None

class NoArrearsCertificateCreate(NoArrearsCertificateBase):
    pass

class NoArrearsCertificateRead(NoArrearsCertificateBase):
    id: int
    barcode: Optional[str] = None
    barcode_url: Optional[str] = None
    gramPanchayat: Optional[str] = None
    taluka: Optional[str] = None
    jilha: Optional[str] = None
    model_config = {
        "from_attributes": True
    } 