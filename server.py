import uvicorn

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    uvicorn.run(
        "main:socketio_app",
        host=host,
        port=port
        # ssl_keyfile="key.pem",
        # ssl_certfile="cert.pem",
    )
# --ssl-keyfile key.pem --ssl-certfile certificate.pem --reload
