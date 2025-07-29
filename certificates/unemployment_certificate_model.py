from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import date

class UnemploymentCertificate(Base):
    __tablename__ = "unemployment_certificates"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    registration_date: Mapped[date] = mapped_column(nullable=False)
    village: Mapped[str] = mapped_column(nullable=True)
    village_en: Mapped[str] = mapped_column(nullable=True)
    applicant_name: Mapped[str] = mapped_column(nullable=True)
    applicant_name_en: Mapped[str] = mapped_column(nullable=True)
    adhar_number: Mapped[str] = mapped_column(nullable=True)
    adhar_number_en: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    barcode: Mapped[str] = mapped_column(nullable=True)
    district_id: Mapped[int] = mapped_column(ForeignKey("districts.id", ondelete="CASCADE"), nullable=True)
    taluka_id: Mapped[int] = mapped_column(ForeignKey("talukas.id", ondelete="CASCADE"), nullable=True)
    gram_panchayat_id: Mapped[int] = mapped_column(ForeignKey("gram_panchayats.id", ondelete="CASCADE"), nullable=True) 