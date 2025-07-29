from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True) 