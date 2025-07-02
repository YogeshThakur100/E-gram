from sqlalchemy import Column, Integer, Boolean, String, Text
from database import Base
class Namuna9Settings(Base):
    __tablename__ = "namuna9_settings"
    id = Column(String, primary_key=True, default="namuna9")
    penalty_percentage = Column(Integer, index=True)
    notice_fee = Column(Integer, index=True)
    warrant_fee = Column(Integer, index=True)
    notes = Column(Text, nullable=True)
    keep_namuna9_date = Column(Boolean, default=False)
    keep_notice_date = Column(Boolean, default=False)
    # Add more fields as needed for section 2/3
    # e.g., previous_year, shakti_option, etc. 