from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from namuna8 import namuna8_model as models, namuna8_schemas as schemas
from database import get_db
from namuna8.mastertab.transfer_apis import PropertyTransferLogDB
import json

router = APIRouter()

@router.get('/recordresponses')
def get_ferfar_record_responses(
    village_id: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """फेरफाराचे रजिस्टर - Get property transfer record responses for all properties using existing data"""
    
    # Get village information
    village_info = {
        "village": None,
        "gramPanchayat": None,
        "jilha": None,
        "taluk": None
    }
    
    # Build query for transfer logs using existing table - NO FILTERING
    query = db.query(PropertyTransferLogDB)
    
    if from_date:
        query = query.filter(PropertyTransferLogDB.date >= from_date)
    
    if to_date:
        query = query.filter(PropertyTransferLogDB.date <= to_date)
    
    # Get all transfer logs
    transfer_logs = query.order_by(PropertyTransferLogDB.date.desc()).all()
    
    # Format the response
    property_transfers = []
    
    for log in transfer_logs:
        try:
            new_owners = json.loads(log.new_owners_json)
            old_owners = json.loads(log.old_owners_json)
        except json.JSONDecodeError:
            new_owners = []
            old_owners = []
        
        # Get property details
        property_details = db.query(models.Property).filter(
            models.Property.anuKramank == log.property_id
        ).first()
        
        if property_details:
            # Get village information separately
            village_data = db.query(models.Village).filter(
                models.Village.id == property_details.village_id
            ).first()
            
            # Format previous owner names
            previous_owner_names = []
            for old_owner in old_owners:
                if old_owner.get('wifeName'):
                    previous_owner_names.append(f"{old_owner.get('name', '')} व {old_owner.get('wifeName', '')}")
                else:
                    previous_owner_names.append(old_owner.get('name', ''))
            
            # Format current owner names
            current_owner_names = []
            for new_owner in new_owners:
                if new_owner.get('wifeName'):
                    current_owner_names.append(f"{new_owner.get('name', '')} व {new_owner.get('wifeName', '')}")
                else:
                    current_owner_names.append(new_owner.get('name', ''))
            
            # Create transfer record using existing data
            transfer_record = {
                "entry_number": log.entry_no,
                "village": village_data.name if village_data else "",
                "transaction_date": log.transaction_date.strftime("%d/%m/%Y") if log.transaction_date else "",
                "roadName": property_details.streetName or property_details.citySurveyOrGatNumber or "",
                "propertyNumber": str(property_details.anuKramank),
                "propertyDescription": f"क्षेत्र: {property_details.totalAreaSqFt} चौ.फूट" if property_details.totalAreaSqFt else "",
                "previousOwnerName": ", ".join(previous_owner_names),
                "currentOwnerName": ", ".join(current_owner_names),
                "modification_reference_remarks": log.doc_note or "",  # Using existing doc_note
                "assessment_register_entry_details": log.register_note or ""  # Using existing register_note
            }
            
            property_transfers.append(transfer_record)
    
    # Group by property number (as per your format)
    grouped_transfers = {}
    for transfer in property_transfers:
        property_num = transfer["propertyNumber"]
        if property_num not in grouped_transfers:
            grouped_transfers[property_num] = []
        grouped_transfers[property_num].append(transfer)
    
    # Build final response
    response = {
        "village": village_info["village"],
        "gramPanchayat": village_info["gramPanchayat"],
        "jilha": village_info["jilha"],
        "taluk": village_info["taluk"]
    }
    
    # Add property transfers grouped by property number
    for property_num, transfers in grouped_transfers.items():
        response[property_num] = transfers
    
    return response 