from fastapi import FastAPI, APIRouter
from chat.use_cases.user_service import UserService
from chat.domain.entities.users import User
from chat.use_cases.message_service import SessionHandler

# Create a router instance
router = APIRouter()


@router.post("/register")
async def register_user(user: User):
    user = await UserService.save(user)

    return user


@router.get("/public-key/{user_id}")
async def get_pk(user_id: str):
    print("getting user public key...")
    print(user_id)
    return await UserService.get_receipient_public_key(user_id)


@router.get("/history/{session_id}")
async def get_history(session_id: str):
    return await SessionHandler.get_history(session_id)


@router.post("/login")
async def login(username: str, password: str):
    pass
