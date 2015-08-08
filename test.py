import json
import pprint
import aiohttp
import asyncio
import logging
import websockets

logger = logging.getLogger("Blockheads")
loop = asyncio.get_event_loop()
BLOCKCHAIN_SCALING = 10 ** (-9)
BLOCKCHAIN_URL = "wss://ws.blockchain.info/inv"
IG_URL = "localhost"


@asyncio.coroutine
def run(test=False):
    blockchain_websocket = yield from websockets.connect(BLOCKCHAIN_URL)
    logger.warn("connecting to {}".format(BLOCKCHAIN_URL))
    connection_text = '{"op": "unconfirmed_sub"}'
    logger.warn("connecting to {}".format(IG_URL))
    # ig_websocket = yield from websockets.connect(IG_URL)
    ig_websocket = None

    yield from blockchain_websocket.send(connection_text)
    while True:
        resp = yield from blockchain_websocket.recv()
        resp_dict = json.loads(resp)
        ip_address = resp_dict['x']['relayed_by']
        amount = BLOCKCHAIN_SCALING * sum([t['value'] for t in resp_dict['x']['out']])
        if test:
            logger.warn(pprint.pformat(resp_dict))
            logger.warn("IP: {0}, amount: {1} BTC".format(ip_address, amount))

        location = yield from geolocate_ip(ip_address)
        if test:
            logger.warn(pprint.pformat(location))
        return
        yield from send_loc_and_amount(location, amount, ig_websocket)


@asyncio.coroutine
def geolocate_ip(location_string):
    url = "http://ip-api.com/json/{}".format(location_string)
    response = yield from aiohttp.request('get', url)
    assert response.status == 200
    body = yield from response.read()
    return json.loads(body.decode('utf-8'))


@asyncio.coroutine
def send_loc_and_amount(location, amount, ig_websocket):
    payload = dict(
        location=location,
        amount=amount
    )
    ig_websocket.send(json.dumps(payload))


loop.run_until_complete(run(test=True))
