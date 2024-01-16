from chat.infra.repositories.user_repository import UserRepository
from chat.infra.repositories.session_repository import SessionRepository
from chat.domain.entities.session import Message
from chat.domain.entities.session import Session
from datetime import datetime
import uuid


class SessionHandler:
    @classmethod
    async def create_session_id(cls):
        return str(uuid.uuid4())

    @classmethod
    async def create_session(cls, users, session_id):
        session = Session(users=users, session_id=session_id)

        SessionRepository.add_session(session)

    @classmethod
    async def get_message(cls, data, sid=None):
        # recipient_id = data.get("recipient_id")
        text = data.get("text")
        key = data.get("key")
        sender = str(data["from"])
        session_id = data["session_id"]
        print("Simmetric key")
        print(key)
        return {
            "text": text,
            "key": key,
            "recipient_sid": sid,
            "sender": sender,
            "session_id": session_id,
        }

    @classmethod
    async def add_message(cls, data):
        text = data["text"]
        sender = str(data["from"])
        recipient = str(data["to"])
        session_id = str(data["session_id"])
        key = data["key"]
        if SessionRepository.get_session_by_id(session_id) is None:
            users = [sender, recipient]
            print(users)
            await cls.create_session(users, session_id)

        timestamp = datetime.now()
        new_message = Message(
            text=text, sender=sender, timestamp=timestamp, key=key
        ).dict()
        SessionRepository.add_message(message=new_message, session_id=session_id)
        return new_message

    @classmethod
    async def get_history(cls, session_id: str):
        session = SessionRepository.get_session_by_id(session_id)
        if session is None:
            return []
        print(session)
        return session["messages"]

    @classmethod
    async def get_sid_user(cls, user_id):
        print("Getting user")
        print(user_id)
        # user_id = user_id['id_']
        user = UserRepository.get_user_by_id(user_id)
        return user["sid"]

    @classmethod
    async def get_sid_by_username(cls, username):
        pass

    @classmethod
    async def register_user(cls, sid, user_id=None):
        user = await UserRepository.add_user(sid)
        register_id = user.restration_id
        return register_id

    @classmethod
    async def unregister_user(cls, sid):
        print(sid)
        # await UserRepository.delete_user(sid)
