from sqlalchemy import Column, Integer, String, Date
from database import Base

class BirthCertificate(Base):
    __tablename__ = "birth_certificates"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    register_date = Column(Date)
    village = Column(String)
    child_name = Column(String)
    child_name_en = Column(String)
    gender = Column(String)
    gender_en = Column(String)
    birth_date = Column(Date)
    birth_place = Column(String)
    birth_place_en = Column(String) 
    mother_name = Column(String)
    father_name = Column(String)
    address_at_birth = Column(String)
    permanent_address = Column(String)
    remark = Column(String)
    panhera = Column(String)
    mother_name_en = Column(String)
    father_name_en = Column(String)
    address_at_birth_en = Column(String)
    permanent_address_en = Column(String)
    remark_en = Column(String)
    qrcode = Column(String, nullable=True)  