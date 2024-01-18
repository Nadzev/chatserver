from fastapi import FastAPI, APIRouter
from chat.use_cases.user_service import UserService
from chat.domain.entities.users import User, UpdatePublicKey
from chat.use_cases.message_service import SessionHandler

# Create a router instance
router = APIRouter()


@router.post("/register")
async def register_user(user: User):
    user = await UserService.save(user)

    return user

# @router.post("/register")
# async def register_user(username:str, password:str):
#     user = User(username=username, password=password)
#     user = await UserService.save(user)
#     return user


@router.get("/public-key/{user_id}")
async def get_pk(user_id: str):
    print("getting user public key...")
    print(user_id)
    return await UserService.get_receipient_public_key(user_id)

@router.put("/update-public-key/{user_id}")
async def update_public_key(update_public_key: UpdatePublicKey):
    print("updating public key...")
    print(update_public_key)
    user_id = update_public_key.user_id
    public_key = update_public_key.public_key
    sid = update_public_key.sid
    return await UserService.update_public_key(user_id, public_key,sid)

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    history = await SessionHandler.get_history(session_id)
    print("history")
    print(history)
    return history


