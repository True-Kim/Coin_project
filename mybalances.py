import sys
import time
import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class MybalancesWorker(QThread):
    dataSent = pyqtSignal(dict)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            f = open("api.txt")
            lines = f.readlines()   # 모든 라인 읽어오기
            access = lines[0].strip()  # 0번째 줄 가져오기 strip()메소드를 사용해 '\n'을 없애기.
            secret = lines[1].strip()
            f.close()

            self.upbit = pyupbit.Upbit(access, secret)
            data  = self.upbit.get_balances()
            time.sleep(0.5)
            if data[0] != None:
                self.dataSent.emit(data[0])

    def close(self):
        self.alive = False

class MybalancesWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-ETH"):
        super().__init__(parent)
        uic.loadUi("Mybalances.ui", self)
        self.ticker = ticker
        
        for i in range(self.tableBalances.rowCount()):
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 1, item_1)

            item_2 = QTableWidgetItem(str(""))
            item_2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 2, item_2)

            item_3 = QTableWidgetItem(str(""))
            item_3.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 3, item_3)

            item_4 = QTableWidgetItem(str(""))
            item_4.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 4, item_4)

            item_5 = QTableWidgetItem(str(""))
            item_5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 5, item_5)


        self.ow = MybalancesWorker(self.ticker)
        self.ow.dataSent.connect(self.updateData)
        self.ow.start()

    def updateData(self, data):
        f = open("api.txt")
        lines = f.readlines()   # 모든 라인 읽어오기
        access = lines[0].strip()  # 0번째 줄 가져오기 strip()메소드를 사용해 '\n'을 없애기.
        secret = lines[1].strip()
        f.close()

        self.upbit = pyupbit.Upbit(access, secret)
        balances = self.upbit.get_balances()
        price = pyupbit.get_current_price(self.ticker)
        for i in range(len(balances)):
            amount = float(balances[i]['avg_buy_price']) * (float(balances[i]['balance']) + float(balances[i]['locked']))#매수금액
            amount2= price * (float(balances[i]['currency']))


            item_0 = self.tableBalances.item(i, 0)
            item_0.setText(f"{balances[i]['currency']}")
            item_1 = self.tableBalances.item(i, 1)
            item_1.setText(f"{balances[i]['balance']}"+f"{balances[i]['currency']}")
            item_2 = self.tableBalances.item(i, 2)
            item_2.setText(f"{balances[i]['avg_buy_price']}"+f"{balances[i]['unit_currency']}")
            item_3 = self.tableBalances.item(i, 3)
            item_3.setText(f"{str(amount2)}")
            item_4 = self.tableBalances.item(i, 4)
            item_4.setText(f"{str(amount)}")
            item_5 = self.tableBalances.item(i, 5)
            item_5.setText(f"{balances[i]['balance']}")


    def closeEvent(self, event):
        self.ow.close()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ow = MybalancesWidget()
    ow.show()
    exit(app.exec_())