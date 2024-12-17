from base64 import b64encode
from datetime import datetime, timedelta
from http.client import HTTPException
import jwt

secret_key = 'ligia'
algoritm='HS256'

def create_token(data:dict):
    expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode = data.copy()  
    to_encode.update({"exp": expire}) 
    try:
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algoritm)
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Error encoding the token: {e}")

def check_token(token:str):
    try:
        payload=jwt.decode(token, secret_key, algorithms=[algoritm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirat")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token nevalid")
    

