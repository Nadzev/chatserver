from pydantic import BaseModel, Field
from typing import List

class GroupCreateRequest(BaseModel):
    group_name: str = Field(..., example="My Group")
    members: List[str] = Field(..., example=["user1_id", "user2_id"])