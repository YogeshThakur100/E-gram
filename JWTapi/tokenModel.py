from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
from database import Base , engine

Base.metadata.create_all(bind=engine)
class license(Base):
    __tablename__ = 'license'
    id = Column(Integer, primary_key=True, autoincrement=True)
    encrypted_license_key = Column(String , nullable=True , unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime , default=None)
