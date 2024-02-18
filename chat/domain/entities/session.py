from datetime import datetime
from typing import Dict, List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str
    sender: str
    key: str
    sender_key: str
    type: str = 'individual'
    

class GroupMessage(BaseModel):
    text: str
    sender: str
    receivers: List[str]
    keys: Dict
    sender_key: str
    type: str = 'group'

class Session(BaseModel):
    # id_: UUID = Field(default_factory=uuid4)
    session_id: str
    users: List[str]
    type: str 
    messages: List[Message | GroupMessage] = []
    type: str
