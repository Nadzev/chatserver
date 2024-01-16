from chat.domain.repositories.user_repository import UserRepositoryInterface
from chat.domain.entities.users import User
import os


from pymongo import MongoClient
import os


class UserRepository(UserRepositoryInterface):
    db_url = os.getenv("DATABASE_URL")
    db_name = "chat-redes"  # Replace with your actual database name
    collection_name = "users"
    client = MongoClient(db_url)
    db = client[db_name]
    collection = db[collection_name]

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.collection.find_one({"id_": user_id})

    @classmethod
    def get_user_by_username(cls, username):
        return cls.collection.find_one({"username": username})

    @classmethod
    def list_users(cls):
        return cls.collection.find()

    @classmethod
    def add_user(cls, user):
        cls.collection.insert_one(user)
        return user

    @classmethod
    def update_sid(cls, username, sid):
        cls.collection.update_one({"username": username}, {"$set": {"sid": sid}})
    
    @classmethod
    def update_public_key(cls, user_id, public_key):
        cls.collection.update_one({"user_id": user_id}, {"$set": {"public_key": public_key}})


    @classmethod
    def delete_user(cls, user_id):
        cls.collection.delete_one({"_id": user_id})


#