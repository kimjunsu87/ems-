# 스레드사용 동작
# pyqt template
# from sqlite3 import connect
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Worker(QThread): #PyQt에서 스레드 사용을 위한 클래스
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):  # 스레드로 동작할 내용이 작성 될 부분
        self.parent.pgbTask.setRange(0, 99)
        for i in range(0, 100):
            print(f'출력>{i}')
            self.parent.pgbTask.setValue(i)
            self.parent.txbLog.append(f'출력 > {i}')

class MyApp(QWidget):  # QMainWindow 변경 필요
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./window/ui/threadTask.ui', self)    # UI 파일 ㅣ변경필요

        self.btnStart.clicked.connect(self.btnStartClicked)
        self.show()

    def btnStartClicked(self):
        th = Worker(self)
        th.start()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
