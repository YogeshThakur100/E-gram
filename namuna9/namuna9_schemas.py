from pydantic import BaseModel
from typing import Optional

class Namuna9YearSetupBase(BaseModel):
    village: str
    year: str
    data_source: str
    notes: Optional[str] = None
    # Add more fields as needed for section 2/3
    # previous_year: Optional[str] = None
    # shakti_option: Optional[str] = None

class Namuna9YearSetupCreate(Namuna9YearSetupBase):
    pass

class Namuna9YearSetupRead(Namuna9YearSetupBase):
    id: int
    class Config:
        orm_mode = True

class Namuna9CarryForward(BaseModel):
    village: str
    from_year: str
    to_year: str
    carry_forward_option: str # e.g., "मागील एकूण चे" ~