from sqlalchemy import Column, Integer, String, Date
from database import Base

class ResidentCertificate(Base):
    __tablename__ = "resident_certificates"
    id = Column(Integer, primary_key=True, index=True)
    dispatch_no = Column(String)
    date = Column(Date)
    village = Column(String)
    village_en = Column(String)
    applicant_name = Column(String)
    applicant_name_en = Column(String)
    adhar_no = Column(String)
    adhar_no_en = Column(String)
    image_url = Column(String)
    barcode = Column(String, nullable=True) 