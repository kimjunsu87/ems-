## PYQT 학습
from PyQt5.QtWidgets import *
import sys

def run():
    app = QApplication(sys.argv)  # 1app 객체 생성

    wnd = QMainWindow()  # 2 window 객체 생성, QWidget, QDialog 중 골라쓰면 된다
    label = QLabel('\tHello, Qt5!!')  # 라벨위젯 생성
    wnd.setWindowTitle('First PyQt')
    wnd.resize(500, 300)
    wnd.setCentralWidget(label)  # 윈도우 정중앙 위치
    wnd.show()  # 3

    app.exec_()  # 4

if __name__ == '__main__' :
    run()

