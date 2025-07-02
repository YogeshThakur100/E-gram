from sqlalchemy import Column, Integer, String, Date
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
    relation_type = Column(String, nullable=True)
    # Add more fields as needed for the form 