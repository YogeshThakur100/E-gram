from fastapi import APIRouter , Depends
from fastapi.responses import JSONResponse
from Utility.JWTUtil import create_license_token , verify_license_token , encrypt_token , decrypt_token
from JWTapi import tokenModel as models
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
from cryptography.fernet import InvalidToken

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
            decrypted_key = decrypt_token(license_key)
            try:
                new_license = models.license(
                    encrypted_license_key = decrypted_key
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
                            "decrypted_license_key" : decrypted_key,
                            "encrypted_license_key" : license_key
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
        encrypted_license_key = license.license_key
        decrypted_license_key = decrypt_token(encrypted_license_key)
        print('encrypted_license_key' , encrypted_license_key)
        try:
            decrypted_license_key_valid = db.query(models.license).filter(models.license.encrypted_license_key == decrypted_license_key).first().encrypted_license_key
        except Exception as e:
            return JSONResponse(
                status_code=200,
                content={
                    "success" : False,
                    "message" : "Erorr verify the key",
                    "data" : []
                }
            )
        print("encrypted_license_key_valid" , decrypted_license_key_valid)
        if (decrypted_license_key_valid):
            return JSONResponse(
                status_code=200,
                content={
                    "success" : True,
                    "message" : "License Verified Successfully",
                    "data" : []
                }
            )
        else:
            return JSONResponse(
                status_code=401,
                content={
                    "success" : False,
                    "message" : "License Not Verified, not authorized to move forward",
                    "data" : []
                }
            )
    except InvalidToken:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Invalid license key",
                "data": []
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success" : False,
                "message" : f"Internal server error {str(e)}",
                "data" : []
            }
        )