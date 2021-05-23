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
        uic.loadUi("source/Mybalances.ui", self)
        self.ticker = ticker

        for i in range(self.tableBalances.rowCount()):
            item_0 = QTableWidgetItem(str(""))
            item_0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 0, item_0)

            item_1 = QTableWidgetItem(str(""))
            item_1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tableBalances.setItem(i, 1, item_1)

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

        for i in range(len(balances)):
            item_0 = self.tableBalances.item(i, 0)
            item_0.setText(f"{balances[i]['currency']}")
            item_1 = self.tableBalances.item(i, 1)
            item_1.setText(f"{balances[i]['balance']}")
            item_2 = self.tableBalances.item(i, 0)
            item_2.setText(f"{balances[i]['currency']}")
            item_3 = self.tableBalances.item(i, 1)
            item_3.setText(f"{balances[i]['balance']}")
            item_4 = self.tableBalances.item(i, 0)
            item_4.setText(f"{balances[i]['currency']}")
            item_5 = self.tableBalances.item(i, 1)
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