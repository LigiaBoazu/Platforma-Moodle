from base64 import b64encode
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

secret_key = 'ligia'
algoritm='HS256'
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def create_token(data:dict):
    expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode = data.copy()  
    to_encode.update({"exp": expire}) 
    try:
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algoritm)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=500, detail="Eroare la generare token")

def check_token(token:str):
    try:
        payload=jwt.decode(token, secret_key, algorithms=[algoritm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirat")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token nevalid")
    
def validate_token(token:str = Depends(oauth2_scheme)):
    try:
        payload=check_token(token)
        username=payload.get("sub")
        role=payload.get("role")
        if not username or not role:
            raise HTTPException(status_code=401, detail="Utilizator sau rol incorect")
        return{"username": username, "role":role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirat")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Eroare la validare: {str(e)}")
    

