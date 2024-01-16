from motor.motor_asyncio import AsyncIOMotorClient
from chat.domain.repositories.user_repository import UserRepositoryInterface
from chat.domain.entities.users import User
import os


from pymongo import MongoClient
import os


class SessionRepository(UserRepositoryInterface):
    db_url = os.getenv("DATABASE_URL")
    db_name = "chat-redes"  # Replace with your actual database name
    collection_name = "sessions"
    client = MongoClient(db_url)
    db = client[db_name]
    collection = db[collection_name]

    @classmethod
    def get_session_by_id(cls, session_id):
        session = cls.collection.find_one({"session_id": session_id})
        return session

    @classmethod
    def add_message(cls, session_id, message):
        cls.collection.update_one(
            {"session_id": session_id}, {"$push": {"messages": message}}
        )

    @classmethod
    def add_session(cls, session):
        cls.collection.insert_one(session.dict())
        return session

    @classmethod
    def delete_user(cls, session_id):
        cls.collection.delete_one({"_id": session_id})
