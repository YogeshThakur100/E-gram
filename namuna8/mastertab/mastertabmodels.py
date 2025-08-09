from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
import datetime
from database import Base
import uuid

from sqlalchemy.orm import Mapped, mapped_column


class GeneralSetting(Base):
    __tablename__ = 'generalSetting'

    id = Column(String, primary_key=True, unique=True, nullable=False)
    typingLanguage = Column(String, nullable=True)
    capitalFormula1 = Column(Boolean, nullable=True, default=False)
    capitalFormula2 = Column(Boolean, nullable=True, default=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class NewYojna(Base):
    __tablename__ = 'newYojna'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    yojnaName = Column(String, nullable=False)
    yojnaDescription = Column(String, nullable=True)
    consession = Column(String, nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=True)
    taluka_id = Column(Integer, ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id = Column(Integer, ForeignKey("gram_panchayats.id"), nullable=True)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class BuildingUsageWeightage(Base):
    __tablename__ = "building_usage_weightage"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    serial_number: Mapped[int] = mapped_column()
    building_usage: Mapped[str] = mapped_column()
    weightage: Mapped[float] = mapped_column()
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id"), nullable=True)
    taluka_id: Mapped[int] = mapped_column(ForeignKey("talukas.id"), nullable=True)
    gram_panchayat_id: Mapped[int] = mapped_column(ForeignKey("gram_panchayats.id"), nullable=True)
