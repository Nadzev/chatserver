import socketio
import asyncio

print("oiiiiiiiiiiiiiiiii")
sio = socketio.AsyncClient()

# sio2 = socketio.AsyncClient()
# await sio.emit('sensor',payload)


async def send():
    msg = "hello"
    to = "my_user_id"
    recipient_id = "my_user_id2"
    text = f"hello {recipient_id}"
    key = "13i3iq0i309"
    data = {"text": text, "key": key, "recipient_id": recipient_id}
    # time.sleep(3)
    await sio.emit("message", data)


@sio.on("message")
def on_message(data):
    print(data)
    print("I received a message!")


async def connect():
    await sio.connect("http://0.0.0.0:8000")
    payload = {}
    payload["type"] = "@sensor/REQUEST_MONITOR_START"
    await sio.emit("register", "my_user_id3")
    await send()
    # await sio2.emit('register', 'my_user_id2')

    await send()
    print("connected")


# @sio.on('sensor')
# def on_connect(data):
#     print(data)
#     print("I'm connected to the /chat namespace!")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(connect())
    loop.run_forever()
