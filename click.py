import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic
from PyQt5.uic import loadUi
import pyupbit
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

click = 'click.ui'

class MainDialog(QDialog):
    def __init(self):
        QDialog.__init__(self, None)
        uic.loadUi(click, self)

        self.num_pushButton_1.clicked.connect(self.buyETH)

    def buyETH(self):
        access_key = 'jwQlJv1VmsZHeXjEW9aqO0zITZVrYz2TCrgJgxxO'
        secret_key = 'xokyR6STrCmU0Hzt30pE009j3AOnq655dKVJJYpJ'

        query = {
            'market': 'KRW-ETH', #이더리움
            'side': 'bid', #bid 매수 ask 매도
            'volume': '0.01',
            'price': '100.0',
            'ord_type': 'price', #시장가 매수
        }
        query_string = urlencode(query).encode()

        m = hashlib.sha512() #암호화
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
