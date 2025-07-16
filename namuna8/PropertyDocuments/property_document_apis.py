from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from .property_document_model import PropertyDocument
from .property_document_schemas import PropertyDocumentCreate, PropertyDocumentResponse
from typing import List
import shutil
import os

router = APIRouter(prefix="/namuna8/property_documents", tags=["PropertyDocuments"])

UPLOAD_DIR = "uploaded_images/property_documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=PropertyDocumentResponse)
def create_property_document(doc: PropertyDocumentCreate, db: Session = Depends(get_db)):
    db_doc = PropertyDocument(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("/", response_model=List[PropertyDocumentResponse])
def list_property_documents(property_anuKramank: int, db: Session = Depends(get_db)):
    return db.query(PropertyDocument).filter(PropertyDocument.property_anuKramank == property_anuKramank).all()

@router.delete("/{doc_id}")
def delete_property_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(PropertyDocument).get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"ok": True}

@router.post("/upload_image/", response_model=str)
def upload_document_image(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_file"
    file_location = os.path.join(UPLOAD_DIR, filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location 