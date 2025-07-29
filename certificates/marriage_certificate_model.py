from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import date

class MarriageCertificate(Base):
    __tablename__ = "marriage_certificates"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    registration_date: Mapped[date] = mapped_column(nullable=False)
    village: Mapped[str] = mapped_column(nullable=True)
    village_en: Mapped[str] = mapped_column(nullable=True)
    husband_name: Mapped[str] = mapped_column(nullable=True)
    husband_name_en: Mapped[str] = mapped_column(nullable=True)
    husband_adhar: Mapped[str] = mapped_column(nullable=True)
    husband_adhar_en: Mapped[str] = mapped_column(nullable=True)
    husband_address: Mapped[str] = mapped_column(nullable=True)
    husband_address_en: Mapped[str] = mapped_column(nullable=True)
    wife_name: Mapped[str] = mapped_column(nullable=True)
    wife_name_en: Mapped[str] = mapped_column(nullable=True)
    wife_adhar: Mapped[str] = mapped_column(nullable=True)
    wife_adhar_en: Mapped[str] = mapped_column(nullable=True)
    wife_address: Mapped[str] = mapped_column(nullable=True)
    wife_address_en: Mapped[str] = mapped_column(nullable=True)
    marriage_date: Mapped[date] = mapped_column(nullable=False)
    marriage_register_no: Mapped[str] = mapped_column(nullable=True)
    marriage_register_subno: Mapped[str] = mapped_column(nullable=True)
    marriage_place: Mapped[str] = mapped_column(nullable=True)
    marriage_place_en: Mapped[str] = mapped_column(nullable=True)
    remark: Mapped[str] = mapped_column(nullable=True)
    remark_en: Mapped[str] = mapped_column(nullable=True)
    barcode: Mapped[str] = mapped_column(nullable=True)
    qrcode: Mapped[str] = mapped_column(nullable=True)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="CASCADE"), nullable=True)
    taluka_id: Mapped[int] = mapped_column(ForeignKey("talukas.id", ondelete="CASCADE"), nullable=True)
    gram_panchayat_id: Mapped[int] = mapped_column(ForeignKey("gram_panchayats.id", ondelete="CASCADE"), nullable=True) 