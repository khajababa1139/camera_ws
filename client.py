import asyncio
import websockets
import cv2
import numpy as np
import sys
import time

SERVER_IP = "127.0.0.1"  # Change to your server's IP if needed
SERVER_PORT = 8765        # Change if needed

async def receive_stream(uri):
    while True:
        try:
            async with websockets.connect(uri, max_size=2**24) as websocket:
                print(f"Connected to {uri}")
                while True:
                    try:
                        data = await websocket.recv()
                        if isinstance(data, str):
                            print(f"Server message: {data}")
                            if "Failed to open camera" in data:
                                break
                            continue
                        # Decode JPEG bytes to image
                        np_arr = np.frombuffer(data, np.uint8)
                        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                        if frame is not None:
                            cv2.imshow("WebSocket Camera Stream", frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                print("Exiting viewer.")
                                return
                        else:
                            print("Failed to decode frame.")
                    except Exception as e:
                        print(f"Error receiving frame: {e}")
                        break
        except (websockets.exceptions.ConnectionClosedError, ConnectionRefusedError) as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        print("Reconnecting in 3 seconds...")
        time.sleep(3)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        SERVER_IP = sys.argv[1]
        SERVER_PORT = int(sys.argv[2])
    uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
    try:
        asyncio.run(receive_stream(uri))
    except KeyboardInterrupt:
        print("\n[Exit] Client interrupted by user.")
    finally:
        cv2.destroyAllWindows()