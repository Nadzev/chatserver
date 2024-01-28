import asyncio
import time

import socketio

sio = socketio.AsyncClient()
sio2 = socketio.AsyncClient()

registration_id = None


@sio.event
async def connect():
    print("connected to server")
    # time.sleep(3)
    # await sio.emit('register', 'my_user_id')  # Register with a unique user ID
    # await sio2.emit('register', 'my_user_id2')
    # await send()


@sio.event
async def disconnect():
    print("disconnected from server")


@sio.event
async def message(data):
    print("Message received:", data)  # Handle incoming message


@sio.on("user-registration")
async def receive_id(data):
    print("Message received:", data)  # Handle incoming message


async def send():
    msg = "hello"
    to = "my_user_id"
    recipient_id = "my_user_id2"
    text = f"hello {recipient_id}"
    key = "13i3iq0i309"
    data = {"text": text, "key": key, "recipient_id": recipient_id}
    time.sleep(3)
    await sio2.emit("/message", data)


async def main():
    await sio.connect("http://0.0.0.0:8000")
    time.sleep(3)
    await sio.emit("register", registration_id)  # Register with a unique user ID
    # await sio2.emit('register', 'my_user_id2')
    # await sio.wait()  # Wait for messages
    # await send()


asyncio.run(main())
