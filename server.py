import json
import pprint
import aiohttp
import asyncio
import logging
import websockets

logger = logging.getLogger("Blockheads")
logger.setLevel(logging.DEBUG)
loop = asyncio.get_event_loop()
BLOCKCHAIN_SCALING = 10 ** (-9)
BLOCKCHAIN_URL = "wss://ws.blockchain.info/inv"

clients = []


@asyncio.coroutine
def add_client(websocket, path):
    print("new connection made from {}".format(path))
    clients.append(websocket)
    while True:
        yield


@asyncio.coroutine
def get_transactions():
    blockchain_websocket = yield from websockets.connect(BLOCKCHAIN_URL)
    print("connecting to {}".format(BLOCKCHAIN_URL))
    connection_text = '{"op": "unconfirmed_sub"}'
    yield from blockchain_websocket.send(connection_text)

    while True:
        resp = yield from blockchain_websocket.recv()
        resp_dict = json.loads(resp)
        ip_address = resp_dict['x']['relayed_by']
        amount = BLOCKCHAIN_SCALING * sum([t['value'] for t in resp_dict['x']['out']])
        pprint.pprint(resp_dict)
        print("IP: {0}, amount: {1} BTC".format(ip_address, amount))

        location = yield from geolocate_ip(ip_address)
        pprint.pprint(location)
        if location['status'] != 'success':
            continue

        payload = dict(
            lat=location['lat'],
            lng=location['lon'],
            amount=amount
        )
        pprint.pprint(payload)

        for client in clients:
            if client and client.open:
                yield from client.send(json.dumps(payload))


@asyncio.coroutine
def geolocate_ip(location_string):
    url = "http://ip-api.com/json/{}".format(location_string)
    response = yield from aiohttp.request('get', url)
    assert response.status == 200
    body = yield from response.read()
    return json.loads(body.decode('utf-8'))


start_server = websockets.serve(add_client, 'localhost', 8765)
loop.run_until_complete(start_server)
loop.run_until_complete(get_transactions())
loop.run_forever()
