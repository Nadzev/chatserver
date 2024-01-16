from pydantic import BaseModel, Field
from uuid import UUID
from uuid import UUID, uuid4
from typing import Union, Dict


class User(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    sid: str = None
    public_key: Union[str, Dict]
    username: str


class UsersStorage:
    users = {}
