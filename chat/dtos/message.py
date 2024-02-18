from pydantic import BaseModel


class Message(BaseModel):
    text: str
    sender: str
    receiver: str
    sender_key: str
    session_id: str
    recipient_sid: str
    key: str

