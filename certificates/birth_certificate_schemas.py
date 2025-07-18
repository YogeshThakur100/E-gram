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
    gender_en: Optional[str]
    panhera: Optional[str]
    birth_date: Optional[date]
    birth_place: Optional[str]
    birth_place_en: Optional[str]
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
    barcode: str | None = None

class BirthCertificateCreate(BirthCertificateBase):
    id: Optional[int] = None

class BirthCertificateRead(BirthCertificateBase):
    id: int
    qrcode: str | None = None
    barcode: str | None = None
    barcode_url: str | None = None
    gramPanchayat: str | None = None
    taluka: str | None = None
    jilha: str | None = None
    model_config = {
        "from_attributes": True
    } 