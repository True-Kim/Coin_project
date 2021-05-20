import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtChart import QLineSeries, QChart   #QChart가 도화지라면 QLineSeries는 도화지에 그려질 선
from PyQt5.QtGui import QPainter #Antialiasing을 제거하는데 사용하는 모듈을 import
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
import time
import pyupbit
from PyQt5.QtCore import QThread, pyqtSignal




class PriceWorker(QThread):
    dataSent = pyqtSignal(float)  #데이터를 전달하기 위해 정의

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True  #안전하게 종료하기 위해 인스턴스 변수를 사용, alive의 초깃값은 True

    def run(self):
        while self.alive:  #반복해서 현재가를 조회
            data  = pyupbit.get_current_price(self.ticker)
            time.sleep(1)
            self.dataSent.emit(data)

    def close(self):
        self.alive = False  #close 메서드가 호출되면 alive 변수가 False로 변경



class ChartWidget(QWidget):   #추후 메인 GUI에 추가할 목적이므로 QWidget 클래스를 상속 ChartWidget클래스를 정의
    def __init__(self, parent=None, ticker="KRW-ETH"):   #파라미터 parent는 위젯이 그려질 위치를 지정하는데 사용, 입력하지 않으면 None #티커는 조회할 코인의 종류를 지정
        super().__init__(parent)
        uic.loadUi("chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 128  #라인 차트로 그릴 데이터의 수를 미리 정의

        self.pw = PriceWorker(ticker)
        self.pw.dataSent.connect(self.appendData)
        self.pw.start()

        self.priceData = QLineSeries()  #QLineSeries 객체의 append메서드로 출력할 데이터의 좌표를 x, y 순서대로 입력
        self.priceChart = QChart()  #데이터를 차트 객체로 전달해서 시각화 
        #QChart를 사용해 차트의 타이틀을 입력하거나 범례를 추가하는 등의 일을 할 수 있음
        self.priceChart.addSeries(self.priceData) 
        self.priceChart.legend().hide()  #차트의 범례를 숨김

        axisX = QDateTimeAxis()  #PyChart에서 날짜 축을 관리하는 QDateTimeAxis 객체를 생성
        axisX.setFormat("hh:mm:ss")  #"시:분:초" 형태로 차트에 표시
        axisX.setTickCount(4) #표시할 날짜의 개수를 4로 지정
        dt = QDateTime.currentDateTime() #현재 시간 정보를 QDateTime 객체로
        axisX.setRange(dt, dt.addSecs(self.viewLimit))  #X축에 출력될 값의 범위를 현재 시간부터 viewLimit (120)초 이후까지 설정, 지정된 초 이후의 시간을 QDateTime으로 반환

        axisY = QValueAxis()  #정수를 저장하는 축을 생성
        axisY.setVisible(False)      #축의 레이블을 차트에 표시하지 않음

        #X, Y축을 차트와 데이터에 연결
        self.priceChart.addAxis(axisX, Qt.AlignBottom)  
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0) #여백을 최소화

    def closeEvent(self, event):
        self.pw.close()

    def appendData(self, currPirce):
        if len(self.priceData) == self.viewLimit :  #정해진 데이터 개수만큼 저장돼 있다면
            self.priceData.remove(0)  #오래된 0번 인덱스의 데이터를 삭제
        dt = QDateTime.currentDateTime()  #간과 현재가 (currPrice)를 함께 저장
        self.priceData.append(dt.toMSecsSinceEpoch(), currPirce)
        self.__updateAxis()  #차트의 축정보를 업데이트하는 __updateAxis() 메서드를 호출

    def __updateAxis(self):
        #pointsVector 메서드를 사용해서 QLineSeries 객체에 저장된 데이터를 리스트로 얻어 옴
        pvs = self.priceData.pointsVector() 
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x())) #가장 오래된 0번 인덱스 x 좌표에 저장된 값을 가져옴
        if len(self.priceData) == self.viewLimit :
           dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x())) #마지막 데이터는 119 번 인덱스에 저장 = 최근 시간 정보가 들어 있는 마지막 객체를 선택
        else:
           dtLast = dtStart.addSecs(self.viewLimit) #viewLimit 보다 작다면 시작 위치 0번을 기준으로 viewLimit 초 이후까지 출력
           
        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)

        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))


        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)  #차트에 anti-aliasing을 적용



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)  #이벤트 루프 사이에서 위젯을 생성
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())

    