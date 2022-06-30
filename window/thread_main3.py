# 스레드사용/ 커스텀 시그널 동작
# pyqt template
# from sqlite3 import connect
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


class Worker(QThread): #PyQt에서 스레드 사용을 위한 클래스
    valChangeSignal = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.working = True

    def run(self):  # 스레드로 동작할 내용이 작성 될 부분
        # self.parent.pgbTask.setRange(0, 99)
        while self.working:
            for i in range(0, 10000):
                print(f'출력>{i}')
                self.valChangeSignal.emit(i)
                time.sleep(0.001)

                # self.parent.pgbTask.setValue(i)
                # self.parent.txbLog.append(f'출력 > {i}')

class MyApp(QWidget):  # QMainWindow 변경 필요

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./window/ui/threadTask.ui', self)    # UI 파일 ㅣ변경필요
        self.btnStart.clicked.connect(self.btnStartClicked)
        #worker 클래스가 가지고 있는 valChangeSignal 설정
        self.th = Worker(self)
        self.th.valChangeSignal.connect(self.updateProgress) # 슬롯 정의

        self.show()

    @pyqtSlot(int)  # @데코레이터
    def updateProgress(self, val):
        self.pgbTask.setValue(val)
        self.txbLog.append(f'출력 > {val}')
        if val == 9999:
            self.th.working = False

    @pyqtSlot(str)
    def updateLog(self, val):
        self.txbLog.append(val)

    @pyqtSlot()
    def btnStartClicked(self):
        self.pgbTask.setRange(0, 9999)
        # th = Worker(self)
        self.th.start()
        self.th.working = True
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
