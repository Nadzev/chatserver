import binascii
import json
import ssl
import time
from datetime import datetime

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chat.domain.entities.session import Message, Session
from chat.ui.routes import router
from chat.service.message_service import SessionHandler
from chat.service.user_service import UserService
from chat.service.group_service import GroupService

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
    groups = await GroupService.list_groups()
    users.extend(groups)
    print(users)
    await sio.emit("usersList", users)

@sio.event
async def disconnect(sid):
    await SessionHandler.unregister_user(sid)


@sio.event
async def update_sid(sid, data):
    await UserService.update_sid(data, sid)


# @sio.event
# async def message(sid, data):
#     # data should contain 'recipient_id' and 'text
#     message = await SessionHandler.get_message(data, sid)
#     recipient = str(data["to"])
#     receiver_sid = await SessionHandler.get_sid_user(recipient)
#     await SessionHandler.add_message(data)
#     print("Sending message to " + receiver_sid)
#     await sio.emit("clientMessage", [message], to=receiver_sid)
#     print("Message sent to " + receiver_sid)

@sio.event
async def send_group_message(sid, data):
    room_name = data['room']
    encrypted_message = data['encrypted_message']
    encrypted_keys_for_members = data['keys']

    # Construct the payload
    message_payload = {
        "encrypted_message": encrypted_message,
        "keys": encrypted_keys_for_members
    }

    # Emit the message payload to all clients in the room
    await sio.emit('group_message', message_payload, room=room_name)


@sio.event
async def message(sid, data):
    # Check if the message is for a group
    is_group = data.get('is_group_message')

    if is_group:
        group_id = data['group_id']
        # Retrieve group members and their public keys
        group_members = await GroupService.get_group(group_id).members
        # Encrypt the symmetric key for each member and send the message
        await SessionHandler.add_message(data)
        # message = {
        #     "encrypted_message":data['text'],

        # }
        for member in group_members:
            # Prepare the message payload with the encrypted message and symmetric key
            receiver_sid = await SessionHandler.get_sid_user(member.id)
            print(f"Sending group message to {receiver_sid}")
            await sio.emit("groupMessage", data, to=receiver_sid)
        
    else:
        # Handle direct messages as before
        recipient = str(data["to"])
        message = await SessionHandler.get_message(data, sid)
        receiver_sid = await SessionHandler.get_sid_user(recipient)
        await SessionHandler.add_message(data)
        print("Sending message to " + receiver_sid)
        await sio.emit("clientMessage", [message], to=receiver_sid)
        print("Message sent to " + receiver_sid)


@sio.event
async def create_group(sid, data):
    group_name = data['group_name']
    members = data['members']
    group_id = data['group_id']  # List of member user IDs
    try:
        new_group = await GroupService.create_group(group_id=group_id, group_name=group_name, members=members)
        await sio.emit('group_created', new_group, room=sid) 
        
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, room=sid)

@sio.event
async def joinGroup(sid, data):
    group_id = data['group_id']
    await sio.enter_room(sid, room=group_id)
    print(f"Socket {sid} joined group {group_id}")


@sio.event
async def sendGroupMessage(sid, data):
    group_id = data['group_id']
    message = data['message']
    # You might want to store the message in the database here
    await sio.emit('groupMessage', message, room=group_id)
    print(f"Message sent to group {group_id}: {message}")
