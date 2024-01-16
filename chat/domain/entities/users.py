from pydantic import BaseModel, Field
from uuid import UUID
from uuid import UUID, uuid4
from typing import Union, Dict, Optional


class User(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    sid: str = None
    public_key: Union[str, Dict] = None
    username: str
    password: str

class UpdatePublicKey(BaseModel):
    user_id: str
    public_key: str

class UsersStorage:
    users = {}
