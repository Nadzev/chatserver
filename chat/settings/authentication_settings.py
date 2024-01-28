import os
from dataclasses import dataclass

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


@dataclass
class AuthenticationSettings:
    secrety_key = os.getenv("SECRET_KEY")
    algorithm = "HS256"
    access_token_expire_minutos = 30
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="chat/login")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
