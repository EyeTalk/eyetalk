import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QDesktopWidget, QStackedWidget
from PyQt5.QtCore import pyqtSlot, QPointF, QRect, Qt
from add_char_8btn import EightBtnAddChar
from keyboard_main_8btn import EightBtnKeyboardMain

class Keyboard_UI(QtWidgets.QMainWindow):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        #self.parent = parent
        sg = QDesktopWidget().screenGeometry()
        self.screen = QPointF(sg.width(), sg.height())
        self.resize(self.screen.x(), self.screen.y())

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        keyMain = EightBtnKeyboardMain(self)
        self.stacked_widget.addWidget(keyMain)
        self.stacked_widget.addWidget(EightBtnAddChar(self,keyMain,["0","1","2","3","4","5","6","7"]))
        self.stacked_widget.addWidget(EightBtnAddChar(self,keyMain,["A","B","C","D","E","F","G"," "]))
        self.stacked_widget.addWidget(EightBtnAddChar(self,keyMain,["H","I","J","K","L","M","N","Backspace"]))
        self.stacked_widget.addWidget(EightBtnAddChar(self,keyMain,["O","P","Q","R","S","T","U","Caps"]))
        self.stacked_widget.addWidget(EightBtnAddChar(self,keyMain,["V","W","X","Y","Z",".","?","!"]))

