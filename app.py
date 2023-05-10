import socket

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Define the Tello drone's IP and port
tello_address = ("192.168.10.1", 8889)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a particular address and port
sock.bind(("", 8889))


@app.post("/executeCommand/")
async def execute_command(command: str):
    if not command:
        raise HTTPException(status_code=400, detail="Command is required")

    try:
        # Send the command to the Tello drone
        sock.sendto(command.encode(), tello_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Command executed successfully"}
