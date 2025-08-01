from fastapi import FastAPI , HTTPException , Depends
from jose import JWTError , jwt
from datetime import datetime , timedelta
from dotenv import find_dotenv , load_dotenv
from cryptography.fernet import Fernet
import os 

load_dotenv(find_dotenv())



# Secret key and algorithm
SECRET_KEY = os.getenv('SECRET_KEY') or "your-secret-key-here-make-it-long-and-secure"
ALGORITHM = os.getenv('ALGORITHM') or "HS256"
FERNET_KEY = os.getenv('FERNET_KEY') or "your-32-byte-base64-encoded-fernet-key-here"
LICENSE_VALIDITY_DAYS = 30

# Only initialize fernet if FERNET_KEY is properly set
if FERNET_KEY and FERNET_KEY != "your-32-byte-base64-encoded-fernet-key-here":
    fernet = Fernet(FERNET_KEY)
else:
    fernet = None


def create_license_token():
    expire = datetime.utcnow() + timedelta(days=LICENSE_VALIDITY_DAYS)
    payload = {
        "issued" : True,
        "exp" : expire
    }
    print("Encrypted key",Fernet.generate_key().decode())
    token = jwt.encode(payload , SECRET_KEY , algorithm=ALGORITHM)
    
    return token

def verify_license_token(token : str):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401 , detail="Invalid or expired license")
    

def encrypt_token(token : str) -> str:
    if fernet is None:
        raise ValueError("Fernet key not properly configured")
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(token : str) -> str:
    if fernet is None:
        raise ValueError("Fernet key not properly configured")
    return fernet.decrypt(token.encode()).decode()

