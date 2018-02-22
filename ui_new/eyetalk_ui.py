import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QDesktopWidget, QStackedWidget
from PyQt5.QtCore import pyqtSlot, QPointF, QRect, Qt, QTimer
from calibration import Calibration
from main_8btn import EightBtnMain
from keyboard_main_8btn import EightBtnKeyboardMain


class Top(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        sg = QDesktopWidget().screenGeometry()
        self.screen = QPointF(sg.width(), sg.height())
        self.resize(self.screen.x(), self.screen.y())

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(Calibration(self))
        self.stacked_widget.addWidget(EightBtnMain(self))
        self.stacked_widget.addWidget(EightBtnKeyboardMain(self))
        self.stacked_widget.setCurrentIndex(1)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Top()
    w.show()
    sys.exit(app.exec_())
