from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
import datetime
from database import Base
import uuid


class GeneralSetting(Base):
    __tablename__ = 'generalSetting'

    id = Column(String, primary_key=True, unique=True, nullable=False)
    typingLanguage = Column(String, nullable=True)
    capitalFormula1 = Column(Boolean, nullable=True, default=False)
    capitalFormula2 = Column(Boolean, nullable=True, default=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class NewYojna(Base):
    __tablename__ = 'newYojna'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    yojnaName = Column(String, nullable=False)
    yojnaDescription = Column(String, nullable=True)
    consession = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
