import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import datetime


class District(Base):
    __tablename__ = "districts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Relationship with Taluka
    talukas = relationship("Taluka", back_populates="district", cascade="all, delete-orphan")


class Taluka(Base):
    __tablename__ = "talukas"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column(nullable=True)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Relationships
    district = relationship("District", back_populates="talukas")
    gram_panchayats = relationship("GramPanchayat", back_populates="taluka", cascade="all, delete-orphan")


class GramPanchayat(Base):
    __tablename__ = "gram_panchayats"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column(nullable=True)
    taluka_id: Mapped[int] = mapped_column(ForeignKey("talukas.id", ondelete="CASCADE"))
    image_url: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    
    # Relationships
    taluka = relationship("Taluka", back_populates="gram_panchayats")
    # Note: We'll need to update the existing Property and Owner models to reference gram_panchayat_id instead of village_id 