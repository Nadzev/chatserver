from typing import Dict, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id_: UUID = Field(default_factory=lambda:str(uuid4()))
    sid: str = None
    public_key: Union[str, Dict] = None
    username: str
    password: str
    type: str = 'user'
    old_public_key: Union[str, Dict] = None

class UpdatePublicKey(BaseModel):
    user_id: str
    public_key: Dict
    sid: str
