## LED Control UI
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import RPi.GPIO as GPIO
import time 

BUTTON = 3
RED = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(RED, GPIO.OUT) # 11번 핀 출력셋팅

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    def btnOn_Clicked(self):
        self.label.setText('LED ON!!')
        GPIO.output(RED, GPIO.HIGH)

    def btnOff_Clicked(self):
        self.label.setText('LED OFF')
        GPIO.output(RED, GPIO.LOW)
    def initUI(self):
        self.setWindowTitle('RPi LED Control')
        # 윈도우 기본설정
        self.setGeometry(100, 100, 300, 350)
        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 15))
        self.label.setText('LED Control')
        self.label.setAlignment(Qt.AlignCenter) # 라벨 정중앙

        self.btnOn = QPushButton('LED ON', self)
        self.btnOff = QPushButton('LED OFF', self)

        # 시그널
        self.btnOn.clicked.connect(self.btnOn_Clicked)
        self.btnOff.clicked.connect(self.btnOff_Clicked)

        # self.vbox = QVBoxLayout(self)
        # self.vbox.setAlignment(Qt.AlignCenter)
        # self.vbox.addWidget(self.label)

        self.hbox = QHBoxLayout(self)
        self.hbox.setAlignment(Qt.AlignCenter)
        self.hbox.addWidget(self.btnOn)
        self.hbox.addWidget(self.btnOff)

        self.show()



def closeEvent(self, QCloseEvent):
    GPIO.output(RED, GPIO.LOW)
    GPIO.cleanup()

    self.deleteLater()
    QCloseEvent.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()
    app.exec_()