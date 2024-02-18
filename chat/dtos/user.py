from pydantic import BaseModel
from typing import Dict


class User(BaseModel):
    name: str
    id: str
    password: str


class UpdatePublicKey(BaseModel):
    user_id: str
    public_key: Dict


class UserLogin(BaseModel):
    username: str
    password: str

class SidUpdate(BaseModel):
    user_id:str = None
    sid: str = None
