import json
import pprint
import asyncio
import websockets


@asyncio.coroutine
def hello():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    while True:
        websocket.send('blah')
        lat_lon_amount = yield from websocket.recv()
        stuff = json.loads(lat_lon_amount)
        pprint.pprint(stuff)

asyncio.get_event_loop().run_until_complete(hello())
