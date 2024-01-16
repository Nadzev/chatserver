from abc import ABC, abstractmethod


class UserRepositoryInterface(ABC):
    @classmethod
    @abstractmethod
    async def get_user_by_id(cls, registration_id):
        pass

    @classmethod
    @abstractmethod
    async def add_user(cls, user):
        pass

    @classmethod
    @abstractmethod
    async def delete_user(cls, user_id):
        pass
