from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class DeathCertificate(Base):
    __tablename__ = "death_certificates"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    register_date = Column(Date)
    village = Column(String)
    deceased_name = Column(String)
    deceased_name_en = Column(String)
    gender = Column(String)
    gender_en = Column(String)
    death_date = Column(Date)
    place_of_death = Column(String)
    place_of_death_en = Column(String)
    mother_name = Column(String)
    mother_name_en = Column(String)
    father_name = Column(String)
    father_name_en = Column(String)
    address_at_death = Column(String)
    address_at_death_en = Column(String)
    permanent_address = Column(String)
    permanent_address_en = Column(String)
    remark = Column(String)
    remark_en = Column(String)
    qrcode = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True)   