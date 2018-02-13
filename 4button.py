# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\themi\Desktop\Python GUI\4button.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QPointF, QRect
import pyautogui, time
from multiprocessing import Process


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        self.screen = QPointF(sg.width(), sg.height())
        Frame.resize(self.screen.x(), self.screen.y())
        Frame.setFrameShape(QFrame.StyledPanel)
        Frame.setFrameShadow(QFrame.Raised)
        self.pushButtons = []
        border = self.screen * 0.01
        buttonSize = self.screen / 2.05
        self.pushButton = QPushButton(Frame)
        self.pushButton.setGeometry(QRect(border.x(), border.y(), buttonSize.x(), buttonSize.y()))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.numClicked = 0
        self.pushButton.clicked.connect(self.on_click1)
        self.pushButton_2 = QPushButton(Frame)
        self.pushButton_2.setGeometry(QRect(border.x(), border.y() * 2 + buttonSize.y(), buttonSize.x(), buttonSize.y()))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.numClicked = 0
        self.pushButton_2.clicked.connect(self.on_click2)
        self.pushButton_3 = QPushButton(Frame)
        self.pushButton_3.setGeometry(QRect(border.x() * 2 + buttonSize.x(), border.y() * 2 + buttonSize.y(), buttonSize.x(), buttonSize.y()))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.numClicked = 0
        self.pushButton_3.clicked.connect(self.on_click3)
        self.pushButton_4 = QPushButton(Frame)
        self.pushButton_4.setGeometry(QRect(border.x() * 2 + buttonSize.x(), border.y(), buttonSize.x(), buttonSize.y()))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.numClicked = 0
        self.pushButton_4.clicked.connect(self.on_click4)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    @pyqtSlot()
    def on_click1(self):
        self.pushButton.numClicked += 1
        self.pushButton.setText(str(self.pushButton.numClicked))

    @pyqtSlot()
    def on_click2(self):
        self.pushButton_2.numClicked += 1
        self.pushButton_2.setText(str(self.pushButton_2.numClicked))

    @pyqtSlot()
    def on_click3(self):
        self.pushButton_3.numClicked += 1
        self.pushButton_3.setText(str(self.pushButton_3.numClicked))

    @pyqtSlot()
    def on_click4(self):
        self.pushButton_4.numClicked += 1
        self.pushButton_4.setText(str(self.pushButton_4.numClicked))

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "4 Button"))
        self.pushButton.setText(_translate("Frame", "Top Left"))
        self.pushButton_2.setText(_translate("Frame", "Bottom Left"))
        self.pushButton_3.setText(_translate("Frame", "Bottom Right"))
        self.pushButton_4.setText(_translate("Frame", "Top Right"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fourbutton = QFrame()
    ui = Ui_Frame()
    ui.setupUi(fourbutton)
    fourbutton.showFullScreen()
    sys.exit(app.exec_())
