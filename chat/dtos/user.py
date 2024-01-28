from pydantic import BaseModel
from typing import Dict


class User(BaseModel):
    name: str
    id: str
    password: str


class UpdatePublicKey(BaseModel):
    user_id: str
    public_key: Dict
    sid: str


class UserLogin(BaseModel):
    username: str
    password: str
