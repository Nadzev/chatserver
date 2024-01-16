from chat.infra.repositories.user_repository import UserRepository
from typing import List


class UserService:
    @classmethod
    async def save(cls, user):
        user = user.dict()
        user["id_"] = str(user.get("id_"))
        # public_key_dict = user.get("public_key")
        # public_key = public_key_dict.get("n")
        # user["public_key"] = public_key
        if UserRepository.get_user_by_username(user.get("username")):
            # del user['_id']
            return user

        UserRepository.add_user(user)
        del user["_id"]
        return user

    @classmethod
    async def login(cls, username: str, password: str):
        # Retrieve the user data from the repository
        user = UserRepository.get_user_by_username(username)

        # Check if the user exists
        if not user:
            return {"error": "User not found"}

        # Verify the password (assuming you have a method for this)
        # if not cls.check_password(password, user.get('hashed_password')):
        #     return {"error": "Invalid password"}

        # The login is successful, return the user data
        # Depending on your application's needs, you might want to return only specific fields
        del user["hashed_password"]  # It's a good practice to remove sensitive data
        return user

    @classmethod
    async def get_receipient_public_key(cls, user_id):
        user = UserRepository.get_user_by_id(user_id)
        public_key = user.get("public_key")
        return public_key

    @classmethod
    async def update_sid(cls, username, sid):
        UserRepository.update_sid(username, sid)

    # @classmethod
    # async def list_users(cls):
    #     users = UserRepository.list_users()
    #     users = list(users)
    #     print("list total de usuários")
    #     print(users)
    #     converted_users = []
    #     for user in users:
    #         del user["_id"]
    #         converted_users.append(user)

    #     # print('listing users...')
    #     # print(users)
    #     return converted_users

    @classmethod
    async def list_users(cls) -> List[dict]:
        users = UserRepository.list_users()

        print("Total number of users:")
        print(users)

        converted_users = [cls.remove_id_field(user) for user in users]
        print(converted_users)
        # If you want to print the converted users, uncomment the following lines:
        # print('Listing users...')
        # print(converted_users)

        return converted_users

    @staticmethod
    def remove_id_field(user: dict) -> dict:
        """
        Remove the "_id" field from the user dictionary.
        """
        user_without_id = user.copy()
        user_without_id.pop("_id", None)
        return user_without_id
