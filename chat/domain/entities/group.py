from typing import Dict, Optional, Union, List
from pydantic import BaseModel, Field


class Group(BaseModel):  # Assuming you're using Pydantic models like FastAPI does
    group_id: str
    group_name: str
    members: List[str]
