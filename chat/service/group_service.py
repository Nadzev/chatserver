from typing import List
from chat.domain.entities.group import Group  # Ensure you have a Group entity defined
from chat.infra.repositories.group_repository import (
    GroupRepository,
)  # Assuming the existence of GroupRepository
from chat.infra.repositories.user_repository import UserRepository

class GroupService:
    @classmethod
    async def create_group(cls,group_name: str, members: List[str], session_id) -> Group:
        """
        Create a new group with the specified name and members.

        :param group_name: Name of the group to be created.
        :param members: List of user IDs to be included in the group.
        :return: The created Group object.
        """
        # Generate a unique ID for the group (or you can do this inside the GroupRepository)
        # group_id = str(uuid.uuid4())
        group = Group(username=group_name, members=members, session_id=session_id)
        group.id_ = str(group.id_)
        GroupRepository.create_group(group)
        
        return group.dict()
    
    @classmethod
    async def get_public_keys(cls, group_id: str):
        group = await cls.get_group(group_id)
        members = group['members']
        pair_members = {}
        pair_members['group_id'] = group_id
        pair_members['keys'] = {}
        for member in members:
            user = UserRepository.get_user_by_id(member)
            public_key = user['public_key']
            user_id = user['id_']  # Assuming 'id' is the attribute you can use as a unique identifier for the user
            pair_members['keys'][user_id] = public_key

        return pair_members



    @classmethod
    async def add_member(cls, group_id: str, user_id: str) -> None:
        """
        Add a member to the group.

        :param group_id: ID of the group to add the member to.
        :param user_id: ID of the user to be added to the group.
        """
        GroupRepository.add_member_to_group(group_id, user_id)

    @classmethod
    async def remove_member(cls, group_id: str, user_id: str) -> None:
        """
        Remove a member from the group.

        :param group_id: ID of the group to remove the member from.
        :param user_id: ID of the user to be removed from the group.
        """
        GroupRepository.remove_member_from_group(group_id, user_id)

    @classmethod
    async def get_group(cls, group_id: str) -> Group:
        """
        Retrieve a group by its ID.

        :param group_id: ID of the group to retrieve.
        :return: The Group object.
        """
        # print(GroupRepository.get_group_by_id(group_id))
        return GroupRepository.get_group_by_id(group_id)

    @classmethod
    async def list_groups(cls) -> List[Group]:
        """
        List all groups.

        :return: A list of all Group objects.
        """
        groups = GroupRepository.list_groups()
        converted_users = [cls.remove_id_field(group) for group in groups]

        return converted_users
    
    @classmethod
    async def get_groups_for_user(cls, user_id):
        groups = GroupRepository.get_groups_by_member_id(user_id)
        converted_users = [cls.remove_id_field(group) for group in groups]

        return converted_users
    

    @staticmethod
    def remove_id_field(user: dict) -> dict:
        """
        Remove the "_id" field from the user dictionary.
        """
        user_without_id = user.copy()
        user_without_id.pop("_id", None)
        return user_without_id

    @classmethod
    async def delete_group(cls, group_id: str) -> None:
        """
        Delete a group by its ID.

        :param group_id: ID of the group to delete.
        """
        GroupRepository.delete_group(group_id)

    @classmethod
    async def update_group_name(cls, group_id: str, new_name: str) -> None:
        """
        Update the name of a group.

        :param group_id: ID of the group to update.
        :param new_name: New name for the group.
        """
        GroupRepository.update_group_name(group_id, new_name)
