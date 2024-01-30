import os
from datetime import timedelta
from typing import List

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from chat.domain.entities.users import User
from chat.infra.repositories.user_repository import UserRepository
from chat.settings.authentication_settings import AuthenticationSettings
from chat.utils.authentication import create_access_token, decode_access_token


class UserService:
    @classmethod
    async def get_current_user(
        cls, token: str = Depends(AuthenticationSettings.oauth2_scheme)
    ):
        user = None
        payload = decode_access_token(token)
        email = payload.get("sub")
        user = await cls.get_user(email)
        if user:
            return user
        return None

    @staticmethod
    async def authenticate_user(student, password):
        response = AuthenticationSettings.pwd_context.verify(
            password, student["password"]
        )
        return response

    @staticmethod
    async def get_user(username: str):
        return UserRepository.get_user_by_username(username)

    @classmethod
    async def login(cls, user: User):
        username = user.username
        user = UserRepository.get_user_by_username(username)

        if user is None or not await cls.authenticate_user(user, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token_expires = timedelta(
            minutes=AuthenticationSettings.access_token_expire_minutos
        )
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @classmethod
    async def save(cls, user: User):
        user.id_ = str(user.id_)
        created_user = await UserRepository.create(
            user, AuthenticationSettings.pwd_context
        )
        created_user = created_user.dict()
        print(created_user)
        # del created_user["_id"]
        return created_user

    @classmethod
    async def get_receipient_public_key(cls, user_id):
        print(user_id)
        user = UserRepository.get_user_by_id(user_id)
        public_key = user.get("public_key")
        del user["_id"]
        return user

    @classmethod
    async def update_sid(cls, username, sid):
        UserRepository.update_sid(username, sid)

    @classmethod
    async def update_public_key(cls, user_id, public_key, sid):
        UserRepository.update_public_key(user_id, public_key, sid)

    @classmethod
    async def list_users(cls) -> List[dict]:
        users = UserRepository.list_users()

        converted_users = [cls.remove_id_field(user) for user in users]

        return converted_users

    @staticmethod
    def remove_id_field(user: dict) -> dict:
        """
        Remove the "_id" field from the user dictionary.
        """
        user_without_id = user.copy()
        user_without_id.pop("_id", None)
        return user_without_id
