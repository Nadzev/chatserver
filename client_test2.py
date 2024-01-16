import socketio
import asyncio
import ssl
import requests
import aiohttp


ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.load_verify_locations("cert.pem")
connector = aiohttp.TCPConnector(ssl=ssl_context)
http_session = aiohttp.ClientSession(connector=connector)


# ssl_context = ssl.create_default_context(cafile='certificate.pem')

sio = socketio.AsyncClient(http_session=http_session)


async def send():
    msg = "hello"
    to = "my_user_id"
    recipient_id = "my_user_id1"
    text = f"hello {recipient_id}  again"
    key = "13i3iq0i309"
    data = {"text": text, "key": key, "recipient_id": recipient_id}

    await sio.emit("message", data)


@sio.on("message")
def on_message(data):
    print(data)
    print("I received a message!")


async def connect():
    await sio.connect("https://localhost:8000")
    await sio.emit("register", "my_user_id2")
    await send()

    await send()
    print("connected")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(connect())
    loop.run_forever()
