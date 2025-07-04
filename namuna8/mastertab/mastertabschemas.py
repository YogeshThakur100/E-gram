from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GeneralSettingBase(BaseModel):
    typingLanguage: Optional[str] = None
    capitalFormula1: Optional[bool] = None
    capitalFormula2: Optional[bool] = None

class GeneralSettingCreate(GeneralSettingBase):
    id: str

class GeneralSettingRead(GeneralSettingBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True

class NewYojnaBase(BaseModel):
    yojnaName: str
    yojnaDescription: Optional[str] = None
    consession: Optional[str] = None

class NewYojnaCreate(NewYojnaBase):
    id: int

class NewYojnaRead(NewYojnaBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True 