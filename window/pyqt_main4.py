## QLabel 위젯
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *  # 위젯 속성
from PyQt5.QtCore import *  # Core속성

class MyApp(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()  # 내가 만들 UI 초기화 함수

    def initUI(self):
        self.setWindowTitle('PyQt QLabel')
        #self.move(490, 250)
        #self.resize(300, 300)
        self.setGeometry(800, 400, 320, 280)
        self.setWindowIcon(QIcon('./window/images/lion.png'))

        # Label작업 시작
        label1, label2 = QLabel('LABEL1'), QLabel('라벨2')
        label1.setAlignment(Qt.AlignBottom)
        label1.setStyleSheet(
            ('border-width: 3px;'
            'border-style: solid;'
            'border-color: blue;'
            'image: url(./window/images/image1.png)')
        )
        label2.setAlignment(Qt.AlignBottom)
        label2.setStyleSheet(
            ('border-width: 3px;'
            'border-style: dot-dot-dash;'
            'border-color: red;'
            'image: url(./window/images/image2.png)')
        )

        hbox = QHBoxLayout(self)
        hbox.addWidget(label1)
        hbox.addWidget(label2)

        self.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()

    app.exec_()
