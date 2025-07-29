from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class NoObjectionCertificate(Base):
    __tablename__ = "no_objection_certificates"
    id = Column(Integer, primary_key=True, index=True)
    registration_date = Column(Date, nullable=False)
    village = Column(String, nullable=True)
    village_en = Column(String, nullable=True)
    applicant_name = Column(String, nullable=True)
    applicant_name_en = Column(String, nullable=True)
    adhar_number = Column(String, nullable=True)
    adhar_number_en = Column(String, nullable=True)
    prop_gut_number = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    subject_en = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True) 