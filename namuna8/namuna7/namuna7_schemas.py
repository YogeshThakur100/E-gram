from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class Namuna7Base(BaseModel):
    receiptNumber: int
    receiptBookNumber: int
    reason: Optional[str] = None
    receivedMoney: int
    userId: int
    villageId: int

class Namuna7Create(Namuna7Base):
    pass

class Namuna7Update(BaseModel):
    receiptNumber: Optional[int] = None
    receiptBookNumber: Optional[int] = None
    reason: Optional[str] = None
    receivedMoney: Optional[int] = None
    userId: Optional[int] = None
    villageId: Optional[int] = None

class Namuna7Read(Namuna7Base):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True 