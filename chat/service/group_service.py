from typing import List
from chat.domain.entities.group import Group  # Ensure you have a Group entity defined
from chat.infra.repositories.group_repository import GroupRepository  # Assuming the existence of GroupRepository

class GroupService:
    @classmethod
    async def create_group(cls, group_name: str, members: List[str]) -> Group:
        """
        Create a new group with the specified name and members.

        :param group_name: Name of the group to be created.
        :param members: List of user IDs to be included in the group.
        :return: The created Group object.
        """
        # Generate a unique ID for the group (or you can do this inside the GroupRepository)
        group_id = str(uuid.uuid4())
        group = Group(group_id=group_id, group_name=group_name, members=members)
        GroupRepository.create_group(group)
        return group

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
        return GroupRepository.get_group_by_id(group_id)

    @classmethod
    async def list_groups(cls) -> List[Group]:
        """
        List all groups.

        :return: A list of all Group objects.
        """
        return GroupRepository.list_groups()

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
