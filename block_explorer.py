import requests

__author__ = 'elvijs'


def get_block(block_num):
    return fetch('https://blockchain.info/rawblock/{}'.format(block_num))


def get_tx(tx_hash):
    return fetch('https://blockchain.info/rawtx/{}'.format(tx_hash))


def get_block_txs(block_num):
    data = get_block(block_num)
    return data['tx']


def fetch(url, params=None):
    resp = requests.get(url, params=params)
    if resp.status_code == 200 and resp.json():
        return resp.json()
    else:
        raise Exception("Transaction API fetch error, response text: {}".format(resp.text))


def get_tx_between_times(from_datetime, to_datetime=None):
    pass
