## QPushButton
import sys
from PyQt5.QtWidgets import * # All
from PyQt5.QtGui import *  # 위젯 속성
from PyQt5.QtCore import *  # Core속성

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('QPushButton') 
        self.setGeometry(800, 400, 320, 280)
        self.setWindowIcon(QIcon('./window/images/lion.png'))

        btn1 = QPushButton('Hello', self)
        # btn1.setEnabled(False)
        btn1.clicked.connect(self.btn1_click) # 시그널

        vbox = QVBoxLayout(self)  # , QHBoxLayout, QGridLayout 을 주로 사용
        vbox.addWidget(btn1)

     
        self.show()


def btn1_click(self):  # 슬롯
    QMessageBox.about(self, 'Greeting', 'Hi, everyone~')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()
