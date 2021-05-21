import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
import webbrowser
import pyupbit

class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 로그인 창
        self.ui = uic.loadUi("source/login.ui", self)
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
            self.ui = uic.loadUi("source/new_main2.ui", self)
            self.ui.show()

        # 연결 실패시 실패 메시지 출력
        elif type(mybtc[0]) is dict :
            QMessageBox.information(self, "연결 확인", "연결 실패!")


if __name__ == "__main__":
    # 프로그램 실행 코드
    app = QApplication(sys.argv)
    ow = MainWidget()
    exit(app.exec_())

