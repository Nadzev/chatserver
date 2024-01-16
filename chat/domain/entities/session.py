from pydantic import BaseModel, Field
from typing import List, Union, Dict
from uuid import UUID, uuid4
from datetime import datetime


class Message(BaseModel):
    text: str
    sender: str
    key: str


class Session(BaseModel):
    # id_: UUID = Field(default_factory=uuid4)
    session_id: str
    users: List[str]
    messages: List[Message] = []
