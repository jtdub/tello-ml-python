import asyncio
import socket

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

# Define the Tello drone's IP and port
tello_address = ("192.168.10.1", 8889)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a particular address and port
sock.bind(("", 8889))

# Send initial 'command' to Tello drone to enable SDK mode.
sock.sendto("command".encode(), tello_address)


def send_command(command: str):
    try:
        # Send the command to the Tello drone
        sock.sendto(command.encode(), tello_address)

        # Wait for a response (1024 is the buffer size)
        data, server = sock.recvfrom(1024)
        response = data.decode(encoding="utf-8").strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Command executed successfully", "response": response}


@app.post("/execute/")
async def execute_command(command: str):
    if not command:
        raise HTTPException(status_code=400, detail="Command is required")

    return send_command(command)


@app.post("/takeoff/")
async def takeoff():
    """Take off"""
    return send_command("takeoff")


@app.post("/land/")
async def land():
    """Land"""
    return send_command("land")


@app.post("/stream/")
async def stream(state: bool = True):
    """Enable Video Stream"""
    if state:
        return send_command("streamon")

    return send_command("streamoff")


@app.post("/direction/")
async def direction(
    move: str = Query(
        default=None, enum=["up", "down", "left", "right", "forward", "back"]
    ),
    dist: int = 20,
):
    """
    Move in a direction.
    Directions:
     - up
     - down
     - left
     - right
     - forward
     - back
    Distances are measured in centimeters.
    Distance values:
     - 20 >= 500
    """
    if not move:
        raise HTTPException(status_code=400, detail="A direction is required")

    if not dist:
        raise HTTPException(status_code=400, detail="A distance is required")

    if 20 <= dist <= 500:
        raise HTTPException(
            status_code=400, detail="The distance must be between 20 and 500 cm"
        )

    return send_command(f"{move} {dist}")


@app.post("/rotate/")
async def rotate(move: str = Query(default="cw", enum=["cw", "ccw"]), dist: int = 1):
    """
    Rotate clockwise or counter clockwise
    Direction:
     - cw (clockwise)
     - ccw (counter clockwise)
    Distances are meatured in degrees.
    Distance Values:
     - 1 >= 360
    """
    if not move:
        raise HTTPException(status_code=400, detail="A direction is required")

    if not dist:
        raise HTTPException(status_code=400, detail="A distance is required")

    if 1 <= dist <= 360:
        raise HTTPException(
            status_code=400, detail="The distance must be between 1 and 360 degree"
        )

    return send_command(f"{move} {dist}")
