import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import webbrowser
import pyupbit
from volatility import *
import datetime
import time

class VolatilityWorker(QThread):
    tradingSent = pyqtSignal(str, str, str)

    def __init__(self, ticker, upbit):
        super().__init__()
        self.ticker = ticker
        self.upbit = upbit
        self.alive = True

    def run(self):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5(self.ticker)
        target_price = get_target_price(self.ticker)
        wait_flag = False

        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.delta(seconds=10):
                    target_price = get_target_price(self.ticker)
                    mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    ma5 = get_yesterday_ma5(self.ticker)
                    desc = sell_crypto_currency(self.bithumb, self.ticker)

                    result = self.upbit.get_order_completed(desc)
                    timestamp = result['data']['order_date']
                    dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000) )

                    tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                    self.tradingSent.emit(tstring, "매도", result['data']['order_qty'])

                    wait_flag = False

                if wait_flag == False:
                    current_price = pyupbit.get_current_price(self.ticker)
                    if (current_price > target_price) and (current_price > ma5):
                        desc = buy_crypto_currency(self.bithumb, self.ticker)
                        result = self.bithumb.get_order_completed(desc)
                        timestamp = result['data']['order_date']
                        dt = datetime.datetime.fromtimestamp( int(int(timestamp)/1000000))
                    
                        tstring = dt.strftime("%Y/%m/%d %H:%M:%S")
                        self.tradingSent.emit(tstring, "매수", result['data']['order_qty'])
                        wait_flag = True
            except: pass

            time.sleep(1)


    def close(self):
        self.alive = False


class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 로그인 창
        self.ui = uic.loadUi("login.ui", self)
        self.ui.show()
    
    def slot_linked_browser(self):
        url = "https://upbit.com/service_center/open_api_guide"
        webbrowser.open_new(url)

    # # 종료 이벤트(메시지)
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, '종료 확인', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def slot_window_change(self):
        access = self.ui.lineEdit.text()
        secret = self.ui.lineEdit_2.text()

        with open('api.txt', 'w') as f:
            f.write(access)
            f.write("\n"+ secret)

        upbit = pyupbit.Upbit(access,secret)
        mybtc = upbit.get_balances("KRW-BTC")
        # print(type(mybtc[0]))

        # 연결 성공시 로그인창 닫고 메인창 열기
        if  type(mybtc[0]) is list:
            QMessageBox.information(self, "연결 확인", "연결 성공!")
            self.ui.close()
            self.ui = uic.loadUi("new_main2.ui", self)
            self.ui.show()

        # 연결 실패시 실패 메시지 출력
        elif type(mybtc[0]) is dict :
            QMessageBox.information(self, "연결 확인", "연결 실패!")
        

    def slot_clickStart(self):
        f = open("api.txt")
        lines = f.readlines()   # 모든 라인 읽어오기
        access = lines[0].strip()  # 0번째 줄 가져오기 strip()메소드를 사용해 '\n'을 없애기.
        secret = lines[1].strip()
        f.close()
        
        self.upbit = pyupbit.Upbit(access, secret)
        self.ticker = "KRW-ETH"
        balance = self.upbit.get_balance(self.ticker)
        self.textEdit.append("------ START ------")
        self.vw = VolatilityWorker(self.ticker, self.upbit)
        self.vw.tradingSent.connect(self.receiveTradingSignal)
        self.vw.start()

    def slot_clickStop(self):
        self.vw.close()
        self.textEdit.append("------- END -------")
    
    def receiveTradingSignal(self, time, type, amount):
        self.textEdit.append(f"[{time}] {type} : {amount}")

    def closeEvent(self, event):
        self.close()

if __name__ == "__main__":
    # 프로그램 실행 코드
    app = QApplication(sys.argv)
    ow = MainWidget()
    exit(app.exec_())