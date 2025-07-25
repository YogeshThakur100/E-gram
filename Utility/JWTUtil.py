from fastapi import FastAPI , HTTPException , Depends
from jose import JWTError , jwt
from datetime import datetime , timedelta
from dotenv import find_dotenv , load_dotenv
from cryptography.fernet import Fernet
import os 

load_dotenv(find_dotenv())



# Secret key and algorithm
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
FERNET_KEY = os.getenv('FERNET_KEY')
LICENSE_VALIDITY_DAYS = 30

fernet = Fernet(FERNET_KEY)


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
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(token : str) -> str:
    return fernet.decrypt(token.encode()).decode()

