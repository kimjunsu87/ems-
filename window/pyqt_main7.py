## QSlider, QDial
import sys
from PyQt5.QtWidgets import * # All
from PyQt5.QtGui import *  # 위젯 속성
from PyQt5.QtCore import *  # Core속성

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('QSlider&QDial') 
        self.setGeometry(800, 400, 320, 280)
        self.setWindowIcon(QIcon('./window/images/lion.png'))

        # 슬라이더
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 50)
        self.slider.setSingleStep(10)
        self.slider.setTickPosition(1)

        # 다이얼
        self.dial = QDial(self)
        self.dial.setRange(0, 50)
        self.dial.setSingleStep(5)
        
        self.btn = QPushButton('reset', self)

        # 시그널 정의
        self.slider.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.slider.setValue)
        self.btn.clicked.connect(self.btn_clicked)

        # 화면 구성
 
        vbox = QVBoxLayout(self)  # , QHBoxLayout, QGridLayout 을 주로 사용
        vbox.addWidget(self.slider)
        vbox.addWidget(self.dial)
        vbox.addWidget(self.btn)
     
        self.show()
    
    def btn_clicked(self):
        self.slider.setValue(0)
        self.dial.setValue(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()
