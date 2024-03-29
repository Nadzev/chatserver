from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status

from chat.domain.entities.users import User
from chat.dtos.user import UserLogin, UpdatePublicKey, SidUpdate
from chat.service.message_service import SessionHandler
from chat.service.user_service import UserService
from chat.domain.entities.group import (
    Group,
)  # Make sure this is defined as per your domain model
from chat.service.group_service import (
    GroupService,
)  # Assuming GroupService is implemented as discussed
from typing import List
from chat.dtos.group import GroupCreateRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()


@router.post("/register")
async def register_user(user: User):
    user = await UserService.save(user)
    return user


@router.get("/public-key/{user_id}")
async def get_pk(user_id: str):
    print("Getting public key")
    return await UserService.get_receipient_public_key(user_id)


@router.put("/update-public-key/{user_id}")
async def update_public_key(public_key_data: UpdatePublicKey):
    user_id = public_key_data.user_id
    public_key = public_key_data.public_key
    return await UserService.update_public_key(user_id, public_key)


@router.get("/history/{session_id}")
async def get_history(session_id: str):
    history = await SessionHandler.get_history(session_id)

    return history


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username.lstrip()
    password = form_data.password.lstrip()
    result = await UserService.login(username, password)
    return result


@router.put("/sid/{user_id}")
async def update_sid(data:SidUpdate):
    print(data)
    sid = data.sid
    print(sid)
    user_id = data.user_id
    print(user_id)
    await UserService.update_sid(sid=sid, user_id=user_id)


@router.post("/groups", response_model=Group, status_code=status.HTTP_201_CREATED)
async def create_group(group_create_request: GroupCreateRequest):
    """
    Create a new group with the specified name and members.

    - **group_name**: each group must have a name
    - **members**: list of user IDs to be included in the group
    """
    new_group = await GroupService.create_group(group_name=group_create_request.group_name, members=group_create_request.members, session_id=group_create_request.session_id)
    return new_group

@router.get("/get-groups/{user_id}")
async def get_groups(user_id:str):
    groups = await GroupService.get_groups_for_user(user_id)
    print(groups)
    return groups


@router.get("/group-public-keys/{group_id}")
async def get_public_keys_from_group(group_id: str):
    keys = await GroupService.get_public_keys(group_id)
    print(keys)
    return await GroupService.get_public_keys(group_id)

