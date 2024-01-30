from typing import Dict, Optional, Union, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Group(BaseModel):  # Assuming you're using Pydantic models like FastAPI does
    id_: UUID = Field(default_factory=uuid4)
    username: str
    members: List[str]
    type: str = 'group'
