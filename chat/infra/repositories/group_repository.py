import os
from pymongo import MongoClient
from typing import List

# Assuming a Group domain entity exists similar to the User entity
from chat.domain.entities.group import Group


class GroupRepository:
    db_url = os.getenv("DATABASE_URL")
    db_name = "chat-redes"  # Use your actual database name
    collection_name = "groups"  # Assuming a collection for groups
    client = MongoClient(db_url)
    db = client[db_name]
    collection = db[collection_name]

    @classmethod
    def create_group(cls, group: Group):
        """
        Create a new group in the database.
        """
        cls.collection.insert_one(group.dict())
        return group

    @classmethod
    def get_group_by_id(cls, group_id: str):
        """
        Retrieve a group by its unique ID.
        """
        return cls.collection.find_one({"id_": group_id})

    @classmethod
    def add_member_to_group(cls, group_id: str, user_id: str):
        """
        Add a new member to the specified group.
        """
        cls.collection.update_one(
            {"group_id": group_id}, {"$addToSet": {"members": user_id}}
        )

    @classmethod
    def remove_member_from_group(cls, group_id: str, user_id: str):
        """
        Remove a member from the specified group.
        """
        cls.collection.update_one(
            {"group_id": group_id}, {"$pull": {"members": user_id}}
        )

    @classmethod
    def list_groups(cls) -> List[Group]:
        """
        List all groups in the database.
        """
        return list(cls.collection.find())

    @classmethod
    def delete_group(cls, group_id: str):
        """
        Delete a group by its ID.
        """
        cls.collection.delete_one({"group_id": group_id})

    @classmethod
    def get_groups_by_member_id(cls, user_id: str) -> List[Group]:
        """
        Retrieve all groups that a specific user participates in.
        
        :param user_id: The unique ID of the user.
        :return: A list of Group entities where the user is a member.
        """
        groups = cls.collection.find({"members": user_id})
        # return [Group(**group) for group in groups]
        return list(groups)


    @classmethod
    def update_group_name(cls, group_id: str, new_name: str):
        """
        Update the name of a specified group.
        """
        cls.collection.update_one(
            {"group_id": group_id}, {"$set": {"group_name": new_name}}
        )
