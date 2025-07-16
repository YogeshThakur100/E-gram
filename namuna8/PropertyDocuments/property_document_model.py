from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class PropertyDocument(Base):
    __tablename__ = "property_documents"
    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, nullable=False)
    document_path = Column(String, nullable=True)
    document_image = Column(String, nullable=True)  # Store image path or filename
    property_anuKramank = Column(Integer, ForeignKey("properties.anuKramank"), nullable=False) 