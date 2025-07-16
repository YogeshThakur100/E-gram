from pydantic import BaseModel
from typing import Optional

class PropertyDocumentBase(BaseModel):
    document_name: str
    document_path: Optional[str] = None
    document_image: Optional[str] = None
    property_anuKramank: int

class PropertyDocumentCreate(PropertyDocumentBase):
    pass

class PropertyDocumentResponse(PropertyDocumentBase):
    id: int

    class Config:
        orm_mode = True 