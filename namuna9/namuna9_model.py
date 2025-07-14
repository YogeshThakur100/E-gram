from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey, UniqueConstraint, PickleType
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import uuid

namuna9_property_association = Table(
    "namuna9_property_association",
    Base.metadata,
    Column("namuna9_id", Integer, ForeignKey("namuna9.id")),
    Column("property_id", Integer, ForeignKey("properties.anuKramank"))
)

class Namuna9YearSetup(Base):
    __tablename__ = "namuna9_year_setups"
    id = Column(Integer, primary_key=True, index=True)
    village = Column(String, index=True)
    year = Column(String, index=True)
    data_source = Column(String)
    notes = Column(Text, nullable=True)
    # Add more fields as needed for section 2/3
    # e.g., previous_year, shakti_option, etc. 

class Namuna9(Base):
    __tablename__ = "namuna9"
    __table_args__ = (
        UniqueConstraint("villageId", "yearslap", name="uix_village_yearslap"),
    )
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    yearslap = Column(String(9), nullable=False)
    villageId = Column(String(36), nullable=False)
    grampanchayatId = Column(String(36), nullable=False)
    property_ids = Column(PickleType, nullable=True)  # List of property IDs
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())