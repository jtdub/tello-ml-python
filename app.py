import asyncio
import socket

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Define the Tello drone's IP and port
tello_address = ("192.168.10.1", 8889)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a particular address and port
sock.bind(("", 8889))

# Send initial 'command' to Tello drone to enable SDK mode.
sock.sendto("command".encode(), tello_address)


@app.post("/executeCommand/")
async def execute_command(command: str):
    if not command:
        raise HTTPException(status_code=400, detail="Command is required")

    try:
        # Send the command to the Tello drone
        sock.sendto(command.encode(), tello_address)

        # Wait for a response (1024 is the buffer size)
        data, server = sock.recvfrom(1024)
        response = data.decode(encoding="utf-8").strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Command executed successfully", "response": response}
