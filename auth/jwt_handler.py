import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError
from db_config.connection import settings

SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_SECONDS


def create_access_token(user: str):
    payload = {
        "user": user,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No access token supplied")

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token expired")

        return data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token")
