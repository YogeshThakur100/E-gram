from fastapi import APIRouter , Depends
from fastapi.responses import JSONResponse
from Utility.JWTUtil import create_license_token , verify_license_token , encrypt_token , decrypt_token
from JWTapi import tokenModel as models
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
from cryptography.fernet import InvalidToken
import bcrypt

class license(BaseModel):
    license_key : str

router = APIRouter()
@router.get('/generate-license')
def generate_token():
    try:
        token = create_license_token()
        encrypted_license_key = encrypt_token(token)
        return JSONResponse(
            status_code=200,
            content={
                "success" : True,
                "message" : "License generated successfully",
                "data" : {
                    "license" : encrypted_license_key
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success" : False,
                "message" : str(e),
                "data" : []
            }
        )
        
@router.post('/verify-license')
def verfiy_token(token : str):
    try:
        payload  = verify_license_token(token)
        return JSONResponse(
            status_code=200,
            content={
                "success" : True,
                "message" : "license verified successfully",
                "data" : {
                    "payload" : payload
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success" : False,
                "message" : str(e),
                "data" : []
            }
        )
    
@router.post("/store-encrypted-license")
def store_encrypted_license(license : license , db : Session = Depends(database.get_db)):
    try:
            license_key = license.license_key
            encrypted_key = bcrypt.hashpw(license_key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                new_license = models.license(
                    encrypted_license_key = encrypted_key
                )
                db.add(new_license)
                db.commit()
                db.refresh(new_license)
                db.close()
                return JSONResponse(
                    status_code=200,
                    content={
                        "success" : True,
                        "messgae" : "Encrypted license added successfully",
                        "data" : {
                            "encrypted_license_key" : encrypted_key,
                            "license_key" : license_key
                        }
                    }
                )
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={
                        "success" : False,
                        "message" : f"Error adding in db : {str(e)}",
                        "data" : []
                    }
                )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success" : False,
                "message" : str(e),
                "data" : []
            }
        )

@router.post("/verify-encrypted-license")
def verify_encrypted_license(license : license , db : Session = Depends(database.get_db)):
    try:
        license_key = license.license_key
        licenses = db.query(models.license).all()

        for lic in licenses:
            if bcrypt.checkpw(license_key.encode('utf-8'), lic.encrypted_license_key.encode('utf-8')):
                return JSONResponse(
                    status_code=200,
                    content={
                        "success": True,
                        "message": "License Verified Successfully",
                        "data": []
                    }
                )

        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "License Not Verified, not authorized to move forward",
                "data": []
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal server error: {str(e)}",
                "data": []
            }
        )