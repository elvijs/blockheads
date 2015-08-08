import json
import pprint
import asyncio
import websockets


@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    while True:
        lat_lon_amount = (yield from websocket.recv())
        if lat_lon_amount:
            stuff = json.loads(lat_lon_amount)
            pprint.pprint(stuff)

asyncio.get_event_loop().run_until_complete(hello())
