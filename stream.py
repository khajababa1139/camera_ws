import cv2
import sys
import asyncio
import websockets
import config

async def stream_camera(websocket, path, cam_index):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        await websocket.send("Failed to open camera")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            # Send as bytes
            await websocket.send(buffer.tobytes())
            await asyncio.sleep(0.03)  # ~30 FPS
    finally:
        cap.release()

async def streamer():
    if len(sys.argv) < 2:
        print("Usage: python stream.py <camera_index> <camera_port>")
        sys.exit(1)

    try:
        cam_index = int(sys.argv[1])
    except ValueError:
        print("Camera index must be an integer.")
        sys.exit(1)

    async def handler(websocket, path):
        await stream_camera(websocket, path, cam_index)

    print(f"WebSocket streaming from camera {cam_index} on ws://{config.IP}:8765 ...")
    async with websockets.serve(handler, config.IP, sys.argv[2]):
        await asyncio.Future()  # run forever

try:
    asyncio.run(streamer())
except KeyboardInterrupt:
    print("\n[Exit] Server interrupted by user.")
