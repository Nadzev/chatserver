import uuid
from datetime import datetime

from chat.domain.entities.session import Message, Session, GroupMessage
from chat.infra.repositories.session_repository import SessionRepository
from chat.infra.repositories.user_repository import UserRepository
from chat.infra.repositories.group_repository import GroupRepository
from chat.service.message_service import Message

class SessionHandler:
    @classmethod
    async def create_session_id(cls):
        return str(uuid.uuid4())

    @classmethod
    async def create_session(cls, users, session_id, type):
        session = Session(users=users, session_id=session_id, type=type)
        SessionRepository.add_session(session)

    @classmethod
    async def create_group_session(cls, members, session_id, type):
        session = Session(users=members, session_id=session_id, type=type)
        SessionRepository.add_session(session)


    @classmethod
    async def get_message(cls, data, sid=None):
        text = data.get("text")
        key = data.get("key")
        sender = str(data["from"])
        session_id = data.get("session_id")
        sender_key = data.get("sender_key")
        message = Message(text=text, sender=sender, sender_key=sender_key, key=key, session_id=session_id, recipient_sid=sid)

        return message.dict()
    @classmethod
    async def add_group_message(cls, data):
        print(data)
        text = str(data["text"])
        sender = str(data["from"])
        recipient = str(data["to"])
        session_id = str(data["session_id"])
        sender_key = str(data["sender_key"])
        criptographited_keys = data["keys"]
        print("######received keys#######")
        print(criptographited_keys)
        type = data['type']
        group_id = data['group_id']
        group = GroupRepository.get_group_by_id(group_id)
        members = group['members']
       
        if SessionRepository.get_session_by_id(session_id) is None:
            await cls.create_session(members, session_id,type=type)

        timestamp = datetime.now()
        new_message = GroupMessage(
            text=text,
            sender=sender,
            timestamp=timestamp,
            sender_key=sender_key,
            keys=criptographited_keys,
            receivers=members


        ).dict()
        SessionRepository.add_message(message=new_message, session_id=session_id)
        return new_message


    @classmethod
    async def add_message(cls, data):
        text = str(data["text"])
        sender = str(data["from"])
        recipient = str(data["to"])
        session_id = str(data["session_id"])
        sender_key = str(data["sender_key"])
        key = data["key"]
        type = data['type']
        users = [sender, recipient]

        if SessionRepository.verify_if_exists(users) is None:
           
            await cls.create_session(users, session_id,type=type)

        timestamp = datetime.now()
        new_message = Message(
            text=text,
            sender=sender,
            timestamp=timestamp,
            key=key,
            sender_key=sender_key,
        ).dict()
        SessionRepository.add_message(message=new_message, session_id=session_id)
        return new_message

    @classmethod
    async def get_history(cls, session_id: str):
        session = SessionRepository.get_session_by_id(session_id)
        
        if session is None:
            return []
        return session["messages"]
    
    @classmethod
    async def get_sid_user(cls, user_id):
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
