from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .namuna7_model import Namuna7
from .namuna7_schemas import Namuna7Create, Namuna7Read, Namuna7Update, Namuna7PrintResponse
from typing import List
from database import get_db
from uuid import UUID
from datetime import datetime, timedelta
from ..namuna8_model import Owner, Village, Property

router = APIRouter(prefix="/namuna7", tags=["Namuna7"])

@router.post("/", response_model=Namuna7Read)
def create_namuna7(item: Namuna7Create, db: Session = Depends(get_db)):
    db_item = Namuna7(**item.dict())    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[Namuna7Read])
def get_all_namuna7(
    district_id: int = Query(None, description="Filter by district ID"),
    taluka_id: int = Query(None, description="Filter by taluka ID"),
    gram_panchayat_id: int = Query(None, description="Filter by gram panchayat ID"),
    db: Session = Depends(get_db)
):
    query = db.query(Namuna7)
    if district_id:
        query = query.filter(Namuna7.district_id == district_id)
    if taluka_id:
        query = query.filter(Namuna7.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(Namuna7.gram_panchayat_id == gram_panchayat_id)
    return query.all()

@router.get("/getall_receipts")
def get_namuna7_custom_list(
    startdate: str = Query(..., description="Start date in YYYY-MM-DD format"),
    enddate: str = Query(..., description="End date in YYYY-MM-DD format"),
    district_id: int = Query(None, description="Filter by district ID"),
    taluka_id: int = Query(None, description="Filter by taluka ID"),
    gram_panchayat_id: int = Query(None, description="Filter by gram panchayat ID"),
    db: Session = Depends(get_db)
):
    from datetime import datetime, timedelta
    try:
        start_dt = datetime.strptime(startdate, "%Y-%m-%d")
        end_dt = datetime.strptime(enddate, "%Y-%m-%d") + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    query = db.query(Namuna7).filter(Namuna7.createdAt >= start_dt, Namuna7.createdAt < end_dt)
    if district_id:
        query = query.filter(Namuna7.district_id == district_id)
    if taluka_id:
        query = query.filter(Namuna7.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(Namuna7.gram_panchayat_id == gram_panchayat_id)
    items = query.all()
    result = []
    today = datetime.now().strftime("%d/%m/%Y")
    for idx, item in enumerate(items, start=1):
        owner = db.query(Owner).filter(Owner.id == item.userId).first()
        ownername = owner.name if owner else ""
        village = db.query(Village).filter(Village.id == item.villageId).first()
        grampanchayat = village.name if village else ""
        result.append({
            "grampanchayat": grampanchayat,
            "srNo": idx,
            "receiptDate": item.createdAt.strftime("%Y-%m-%d") if getattr(item, "createdAt", None) else None,
            "receiptNumber": item.receiptNumber,
            "receiptBookNumber": item.receiptBookNumber,
            "village": grampanchayat,
            "ownername": ownername,
            "reason": item.reason or "",
            "receivedMoney": item.receivedMoney,
            "currentDate": today
        })
    return result

@router.get("/{item_id}", response_model=Namuna7Read)
def get_namuna7(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Namuna7).filter(Namuna7.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Namuna7 not found")
    return item

@router.put("/{item_id}", response_model=Namuna7Read)
def update_namuna7(item_id: int, update: Namuna7Update, db: Session = Depends(get_db)):
    item = db.query(Namuna7).filter(Namuna7.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Namuna7 not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_namuna7(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Namuna7).filter(Namuna7.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Namuna7 not found")
    db.delete(item)
    db.commit()
    return {"detail": "Deleted successfully"}

@router.get("/by-date/")
def get_namuna7_by_date(
    from_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    to_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    village_id: int = Query(None, description="Village ID to filter by"),
    district_id: int = Query(None, description="Filter by district ID"),
    taluka_id: int = Query(None, description="Filter by taluka ID"),
    gram_panchayat_id: int = Query(None, description="Filter by gram panchayat ID"),
    db: Session = Depends(get_db)
):
    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    query = (
        db.query(Namuna7, Owner)
        .join(Owner, Namuna7.userId == Owner.id)
        .filter(Namuna7.createdAt >= from_dt, Namuna7.createdAt < to_dt)
    )
    if village_id is not None:
        query = query.filter(Namuna7.villageId == village_id)
    if district_id:
        query = query.filter(Namuna7.district_id == district_id)
    if taluka_id:
        query = query.filter(Namuna7.taluka_id == taluka_id)
    if gram_panchayat_id:
        query = query.filter(Namuna7.gram_panchayat_id == gram_panchayat_id)
    results = query.order_by(Namuna7.createdAt, Namuna7.receiptNumber).all()
    response = [
        {
            **{k: getattr(n7, k) for k in n7.__table__.columns.keys()},
            "date": n7.createdAt.strftime("%Y-%m-%d"),
            "ownerName": owner.name
        }
        for n7, owner in results
    ]
    return response

@router.get("/prints/get/{item_id}", response_model=Namuna7PrintResponse)
def get_namuna7_print(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Namuna7).filter(Namuna7.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Namuna7 not found")
    owner = db.query(Owner).filter(Owner.id == item.userId).first()
    village = db.query(Village).filter(Village.id == item.villageId).first()
    grampanchayat = village.name if village else ""
    ownername = owner.name if owner else ""
    currentDate = datetime.now().strftime("%d/%m/%Y")
    return Namuna7PrintResponse(
        grampanchayat=grampanchayat,
        receiptNumber=int(item.__dict__["receiptNumber"]),
        receiptBookNumber=int(item.__dict__["receiptBookNumber"]),
        village=grampanchayat,
        ownername=ownername,
        reason=str(item.__dict__["reason"]) if item.__dict__["reason"] is not None else "",
        receivedMoney=int(item.__dict__["receivedMoney"]),
        currentDate=currentDate
    ) 

@router.get("/prints/by_village/{village_id}")
def get_namuna7_prints_by_village(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    grampanchayat = village.name if village else ""
    currentDate = datetime.now().strftime("%d/%m/%Y")
    items = db.query(Namuna7).filter(Namuna7.villageId == village_id).all()
    results = []
    for item in items:
        owner = db.query(Owner).filter(Owner.id == item.userId).first()
        ownername = owner.name if owner else ""
        # Find property for this owner in this village (if any)
        property_obj = db.query(Property).filter(Property.village_id == village_id, Property.owners.any(Owner.id == item.userId)).first()
        # anuKramank = property_obj.anuKramank if property_obj else None
        results.append({
            "receiptNumber": int(item.__dict__["receiptNumber"]),
            "receiptBookNumber": int(item.__dict__["receiptBookNumber"]),
            "ownername": ownername,
            "reason": str(item.__dict__["reason"]) if item.__dict__["reason"] is not None else "",
            "receivedMoney": int(item.__dict__["receivedMoney"])
        })
    return {
        "grampanchayat": grampanchayat,
        "village": grampanchayat,
        "currentDate": currentDate,
        "records": results
    } 
    