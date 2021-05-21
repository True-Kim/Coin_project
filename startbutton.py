import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication
import pyupbit
import time
import pprint
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

class Exam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.initUI()   

    """def buy(self):
        access_key = ''
        secret_key = ''

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
"""
    def initUI(self):
        access = ''
        secret = ''
        upbit = pyupbit.Upbit(access, secret)
        btn1 = QPushButton('시작', self)
        btn1.resize(btn1.sizeHint())
        btn1.move(30,50)
        resp = upbit.buy_market_order("KRW-ETH", 5000)
        pprint.pprint(resp)

        btn2 = QPushButton('종료', self)
        btn2.resize(btn1.sizeHint())
        btn2.move(150,50)


        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300,300,290,150)
        self.setWindowTitle('자동 매매 시작/종료')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text()+ '합니다.')


    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, '종료 확인', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Exam()
    sys.exit(app.exec_())


