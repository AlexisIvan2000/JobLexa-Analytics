import time
from datetime import datetime,timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from settings import settings

ALGORITHM = "HS256"
JWT_SECRET = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,JWT_SECRET,algorithms=[ALGORITHM])
        return payload

    except JWTError:
        return None