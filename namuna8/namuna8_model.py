from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

# Association table for many-to-many relationship between Property and Owner
property_owner_association = Table(
    "property_owner_association",
    Base.metadata,
    Column("property_anuKramank", Integer, ForeignKey("properties.anuKramank")),
    Column("owner_id", Integer, ForeignKey("owners.id"))
)

class Owner(Base):
    __tablename__ = "owners"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    aadhaarNumber: Mapped[str] = mapped_column(unique=True, index=True)
    mobileNumber: Mapped[str] = mapped_column(nullable=True)
    wifeName: Mapped[str] = mapped_column(nullable=True)
    occupantName: Mapped[str] = mapped_column(nullable=True)
    ownerPhoto: Mapped[str] = mapped_column(nullable=True)
    streetName: Mapped[str] = mapped_column(nullable=True)
    citySurveyOrGatNumber: Mapped[str] = mapped_column(nullable=True)
    properties = relationship("Property", secondary=property_owner_association, back_populates="owners")

class Property(Base):
    __tablename__ = "properties"
    anuKramank: Mapped[int] = mapped_column(primary_key=True, index=True)
    villageOrMoholla: Mapped[str] = mapped_column()
    malmattaKramank: Mapped[int] = mapped_column(unique=True, index=True)
    citySurveyOrGatNumber: Mapped[str] = mapped_column(nullable=True)
    length: Mapped[float] = mapped_column(nullable=True)
    width: Mapped[float] = mapped_column(nullable=True)
    totalAreaSqFt: Mapped[float] = mapped_column(nullable=True)
    eastBoundary: Mapped[str] = mapped_column(nullable=True)
    westBoundary: Mapped[str] = mapped_column(nullable=True)
    northBoundary: Mapped[str] = mapped_column(nullable=True)
    southBoundary: Mapped[str] = mapped_column(nullable=True)
    divaArogyaKar: Mapped[bool] = mapped_column(default=False)
    safaiKar: Mapped[bool] = mapped_column(default=False)
    shauchalayKar: Mapped[bool] = mapped_column(default=False)
    karLaguNahi: Mapped[bool] = mapped_column(default=False)
    gharKar: Mapped[float] = mapped_column(default=0)
    divaKar: Mapped[float] = mapped_column(default=0)
    aarogyaKar: Mapped[float] = mapped_column(default=0)
    sapanikar: Mapped[float] = mapped_column(default=0)
    vpanikar: Mapped[float] = mapped_column(default=0)
    vacantLandType: Mapped[str] = mapped_column(nullable=True)
    eastBoundary2: Mapped[str] = mapped_column(nullable=True)
    westBoundary2: Mapped[str] = mapped_column(nullable=True)
    northBoundary2: Mapped[str] = mapped_column(nullable=True)
    southBoundary2: Mapped[str] = mapped_column(nullable=True)
    waterFacility1: Mapped[str] = mapped_column(nullable=True)
    waterFacility2: Mapped[str] = mapped_column(nullable=True)
    streetName: Mapped[str] = mapped_column(nullable=True)
    toilet: Mapped[str] = mapped_column(nullable=True)
    roofType: Mapped[str] = mapped_column(nullable=True)
    eastLength: Mapped[float] = mapped_column(nullable=True)
    westLength: Mapped[float] = mapped_column(nullable=True)
    northLength: Mapped[float] = mapped_column(nullable=True)
    southLength: Mapped[float] = mapped_column(nullable=True)
    areaUnit: Mapped[str] = mapped_column(nullable=True)
    constructions = relationship("Construction", back_populates="property", cascade="all, delete-orphan")
    owners = relationship("Owner", secondary=property_owner_association, back_populates="properties")

class Construction(Base):
    __tablename__ = "constructions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    property_anuKramank: Mapped[int] = mapped_column(ForeignKey("properties.anuKramank"))
    constructionType: Mapped[str] = mapped_column()
    length: Mapped[float] = mapped_column()
    width: Mapped[float] = mapped_column()
    constructionYear: Mapped[str] = mapped_column()
    floor: Mapped[str] = mapped_column()
    usage: Mapped[str] = mapped_column()
    bharank: Mapped[str] = mapped_column(nullable=True)
    property = relationship("Property", back_populates="constructions")