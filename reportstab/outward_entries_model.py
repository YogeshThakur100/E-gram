from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from sqlalchemy.sql import func

class OutwardEntry(Base):
    __tablename__ = 'outward_entries'
    
    srNo = Column(String(50), primary_key=True, comment="अ.क्र. / Serial No")
    jaKramank = Column(String(50), nullable=False, unique=True, comment="जा.क्र. / Outward No.")
    reportType = Column(String(100), nullable=False, comment="दस्त प्रकार / Document Type")
    timeNDate = Column(DateTime, nullable=False, comment="दिनांक व वेळ / Date & Time")
    name = Column(String(200), nullable=False, comment="नाव / Name")
    village_id = Column(Integer, default=1, comment="Village ID")
    gram_panchayat_id = Column(Integer, default=1, comment="Gram Panchayat ID")
    district_id = Column(Integer, default=1, comment="District ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Created timestamp")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Updated timestamp")

    def __repr__(self):
        return f"<OutwardEntry(srNo='{self.srNo}', jaKramank='{self.jaKramank}', name='{self.name}')>"

    def to_dict(self):
        return {
            'srNo': self.srNo,
            'jaKramank': self.jaKramank,
            'reportType': self.reportType,
            'timeNDate': self.timeNDate.isoformat() if self.timeNDate else None,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 