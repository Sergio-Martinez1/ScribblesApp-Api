import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ACCESS_TOKEN_EXPIRE_SECONDS = 3600


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
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Token expired")

        return data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token")
