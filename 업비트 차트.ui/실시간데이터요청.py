from requests.api import request
import websocket
import json, time, requests
import hashlib, jwt, uuid
from urllib.parse import urlencode
import os
try:
    from threading import Thread
except ImportError:
    import _thread as thread


access_key = "여기에 입력"
secret_key = '여기에 입력'

def on_message(ws, message):
    json_data = json.loads(message)
    print(json_data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('###closed###')

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(
            [{'ticket':'test'}, {'type':'ticker', 'codes':['KRW-ETH']}]))
        thread.start_new_thread(run, ())

websocket.enableTrace(True)
ws = websocket.WebSocketApp('ws://api.upbit.com/websocket/v1',
                             on_message = on_message,
                             on_error = on_error,
                             on_close = on_close)

ws.on_open = on_open
print(ws.on_open)
ws.run_forever()


