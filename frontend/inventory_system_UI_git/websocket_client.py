import os
import asyncio
import websockets
import json
import threading
from dotenv import load_dotenv

load_dotenv()

WS_URL = os.getenv("WS_URL")


def start_listener(callback):
    def run():
        asyncio.run(_listen(callback))

    thread = threading.Thread(target=run, daemon=True)
    thread.start()


async def _listen(callback):
    try:
        async with websockets.connect(WS_URL) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                callback(data)
    except Exception:
        pass  # silent reconnect optional later