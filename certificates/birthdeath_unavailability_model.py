from sqlalchemy import Column, Integer, String, Date
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
    barcode = Column(String, nullable=True)  # stores the file path for the barcode image 