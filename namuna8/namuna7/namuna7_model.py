from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
from database import Base


class Namuna7(Base):
    __tablename__ = 'namuna7'

    id = Column(Integer, primary_key=True, autoincrement=True)
    receiptNumber = Column(Integer, nullable=False)
    receiptBookNumber = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)
    receivedMoney = Column(Integer, nullable=False)
    userId = Column(Integer, ForeignKey('owners.id'), nullable=False)
    villageId = Column(Integer, ForeignKey('villages.id'), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 