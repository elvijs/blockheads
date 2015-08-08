#!/usr/bin/env python

import asyncio
import websockets
import json

clients = []

@asyncio.coroutine
def server(websocket, path):
    clients.append(websocket)
    while True:
        yield
start_server = websockets.serve(server, 'localhost', 8888)

@asyncio.coroutine
def get_txs():
    websocket = yield from websockets.connect('wss://ws.blockchain.info/inv')
    yield from websocket.send('{"op":"unconfirmed_sub"}')
    while True:
        body = yield from websocket.recv()
        tx = json.loads(body)
        loc = yield from geolocate_ip(tx['x']['relayed_by'])
        #print(tx['x']['relayed_by'])
        print(loc)
        for client in clients:
            yield from client.send(tx)

@asyncio.coroutine
def geolocate_ip(location_string):
    url = "http://ip-api.com/json/{}".format(location_string)
    response = yield from aiohttp.request('get', url)
    assert response.status == 200
    body = yield from response.read()
    return json.loads(body.decode('utf-8'))

asyncio.get_event_loop().create_task(start_server)
asyncio.get_event_loop().create_task(get_txs())
asyncio.get_event_loop().run_forever()
