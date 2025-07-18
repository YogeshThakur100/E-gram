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
    barcode: str | None = None

class BirthDeathUnavailabilityCertificateCreate(BirthDeathUnavailabilityCertificateBase):
    pass

class BirthDeathUnavailabilityCertificateRead(BirthDeathUnavailabilityCertificateBase):
    id: int
    barcode: str | None = None
    barcode_url: str | None = None
    gramPanchayat: str | None = None
    taluka: str | None = None
    jilha: str | None = None
    model_config = {
        "from_attributes": True
    } 