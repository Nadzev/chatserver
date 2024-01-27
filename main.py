import ssl
import socketio
from fastapi import FastAPI
from chat.use_cases.message_service import SessionHandler
from chat.use_cases.user_service import UserService
from fastapi.middleware.cors import CORSMiddleware
from chat.domain.entities.session import Session, Message
from datetime import datetime
import json
from chat.ui.routes import router
import binascii
import time

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],
)

socketio_app = socketio.ASGIApp(sio, other_asgi_app=app)


@sio.event
async def connect(sid, *args):
    print("connect ", sid)
    await sio.emit("getSid", sid, to=sid)
    users = await UserService.list_users()
    await sio.emit("usersList", users)
  


@sio.event
async def disconnect(sid):
    await SessionHandler.unregister_user(sid)

@sio.event
async def update_sid(sid, data):
    await UserService.update_sid(data, sid)
    
@sio.event
async def message(sid, data):
    # data should contain 'recipient_id' and 'text
    print(data)
    message = await SessionHandler.get_message(data, sid)
    recipient = str(data["to"])
    receiver_sid = await SessionHandler.get_sid_user(recipient)
    await SessionHandler.add_message(data)
    print("Sending message to " + receiver_sid)
    await sio.emit("clientMessage", [message], to=receiver_sid)
    print("Message sent to " + receiver_sid)
