from sqlalchemy import Column, Integer, Boolean, String, Text, ForeignKey
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
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True)
    # Add more fields as needed for section 2/3
    # e.g., previous_year, shakti_option, etc. 