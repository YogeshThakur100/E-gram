from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from datetime import datetime
from database import Base

class OwnerHistory(Base):
    __tablename__ = 'owner_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_owner_history_id = Column(Integer, nullable=False)  # Remove foreign key constraint
    entry_number = Column(String(50), nullable=False)  # नोंद क्रमांक
    owner_name = Column(String(255), nullable=False)
    wife_name = Column(String(255), nullable=True)
    owner_id = Column(Integer, nullable=False)  # Remove foreign key constraint
    transferred_to_this_owner_date = Column(Date, nullable=False)  # When this owner got the property
    transferred_from_this_owner_date = Column(Date, nullable=True)  # When this owner transferred to another (NULL for current)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'entry_number': self.entry_number,
            'owner_name': self.owner_name,
            'wife_name': self.wife_name,
            'owner_id': self.owner_id,
            'transferred_to_this_owner_date': self.transferred_to_this_owner_date.isoformat() if self.transferred_to_this_owner_date else None,
            'transferred_from_this_owner_date': self.transferred_from_this_owner_date.isoformat() if self.transferred_from_this_owner_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 