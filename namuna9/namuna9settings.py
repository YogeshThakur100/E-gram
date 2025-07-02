from sqlalchemy import Column, Integer, String, Text
from database import Base
class Namuna9Settings(Base):
    __tablename__ = "namuna9_settings"
    id = Column(Integer, primary_key=True, index=True)
    village = Column(String, index=True)
    year = Column(String, index=True)
    data_source = Column(String)
    notes = Column(Text, nullable=True)
    # Add more fields as needed for section 2/3
    # e.g., previous_year, shakti_option, etc. 