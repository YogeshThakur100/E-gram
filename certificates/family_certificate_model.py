from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class FamilyCertificate(Base):
    __tablename__ = "family_certificates"
    id = Column(Integer, primary_key=True, index=True)
    registration_date = Column(Date, nullable=False)
    village = Column(String, nullable=True)
    village_en = Column(String, nullable=True)
    family_name = Column(String, nullable=True)
    family_name_en = Column(String, nullable=True)
    adhar_number = Column(String, nullable=True)
    adhar_number_en = Column(String, nullable=True)
    record_no = Column(String, nullable=True)
    applicant_name = Column(String, nullable=True)
    applicant_name_en = Column(String, nullable=True)
    relation = Column(String, nullable=True)
    relation_en = Column(String, nullable=True)
    year = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True)
    # Add more fields as needed for the form 