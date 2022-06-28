# QT Designer 연동
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyApp(QMainWindow):

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./window/ui/testwin.ui',self)
        self.dial.valueChanged.connect(self.dial_changed)

        self.show()
    
    def dial_changed(self):
        self.label.setText(str(self.dial.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()