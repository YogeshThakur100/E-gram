from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class BirthDeathUnavailabilityCertificate(Base):
    __tablename__ = "birthdeath_unavailability_certificates"
    id = Column(Integer, primary_key=True, index=True)
    register_date = Column(Date)
    village = Column(String)
    village_en = Column(String)
    applicant_name = Column(String)
    applicant_name_en = Column(String)
    adhar_number = Column(String)
    adhar_number_en = Column(String)
    certificate_name = Column(String)
    certificate_name_en = Column(String)
    subject = Column(String)
    subject_en = Column(String) 
    barcode = Column(String, nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True) 