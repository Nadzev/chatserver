import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from chat.settings.authentication_settings import AuthenticationSettings

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        AuthenticationSettings.secrety_key,
        algorithm=AuthenticationSettings.algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            AuthenticationSettings.secrety_key,
            algorithms=[AuthenticationSettings.algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
