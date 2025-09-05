from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


# --- District Schemas ---
class DistrictBase(BaseModel):
    name: str
    code: Optional[str] = None

class DistrictCreate(DistrictBase):
    pass

class DistrictRead(DistrictBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class DistrictUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


# --- Taluka Schemas ---
class TalukaBase(BaseModel):
    name: str
    code: Optional[str] = None
    district_id: int

class TalukaCreate(TalukaBase):
    pass

class TalukaRead(TalukaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class TalukaUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    district_id: Optional[int] = None


# --- Gram Panchayat Schemas ---
class GramPanchayatBase(BaseModel):
    name: str
    code: Optional[str] = None
    taluka_id: int

class GramPanchayatCreate(GramPanchayatBase):
    pass

class GramPanchayatRead(GramPanchayatBase):
    id: int
    image_url: Optional[str] = None
    from_yearslap: Optional[str] = None
    to_yearslap: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class GramPanchayatUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    taluka_id: Optional[int] = None
    image_url: Optional[str] = None
    from_yearslap: Optional[str] = None
    to_yearslap: Optional[str] = None


# --- Response Schemas with Relationships ---
class DistrictWithTalukas(DistrictRead):
    talukas: List[TalukaRead] = []

class TalukaWithGramPanchayats(TalukaRead):
    gram_panchayats: List[GramPanchayatRead] = [] 