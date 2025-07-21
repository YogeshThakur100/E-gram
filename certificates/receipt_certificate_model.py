from sqlalchemy import Column, Integer, String, Date
from database import Base

class ReceiptCertificate(Base):
    __tablename__ = "receipt_certificates"
    id = Column(Integer, primary_key=True, index=True)
    receipt_date = Column(Date, nullable=False)
    receipt_id = Column(String, nullable=False)
    village = Column(String, nullable=True)
    village_en = Column(String, nullable=True)
    name1 = Column(String, nullable=True)
    name1_en = Column(String, nullable=True)
    name2 = Column(String, nullable=True)
    name2_en = Column(String, nullable=True)
    receipt_amount = Column(String, nullable=True)
    receipt_amount_en = Column(String, nullable=True)
    barcode = Column(String, nullable=True) 