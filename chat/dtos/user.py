from pydantic import BaseModel


class User(BaseModel):
    name: str
    id: str
    password: str
