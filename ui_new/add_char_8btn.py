from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QPointF, QRect

class EightBtnAddChar(QWidget):
    def __init__(self, parent, keyMain, charList):
        QtWidgets.QWidget.__init__(self)
        self.parent = parent
        self.keyMain = keyMain
        self.charList = charList
        self.setupUi()
        
    def goBack(self):
        self.parent.stacked_widget.setCurrentIndex(0)
        self.hide()

    def addChar(self, char):
        new_str = self.keyMain.textBrowser.toPlainText() + char
        self.keyMain.textBrowser.setText(new_str)
        self.parent.stacked_widget.setCurrentIndex(0)
        self.hide()
        
    def setupUi(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        self.screen = QPointF(sg.width(), sg.height())
        self.resize(self.screen.x(), self.screen.y())

	# Calculate borders and button sizes based on screen size
        border = self.screen * 0.05
        btnSizeCir = QPointF(self.screen.x() * 0.1875, self.screen.x() * 0.1875)
        btnSizeCor = self.screen * 0.2

	# Style sheet for buttons
        btnStyleCir = "QPushButton{\n" \
                      "background-color:qlineargradient" \
                      "(x1: 0, y1: 0, x2: 0, y2: 2, stop: 0 white, stop: 1 grey);\n" \
                      "border-style: solid;\n" \
                      "border-color: black;\n" \
                      "border-width: " + str(self.screen.y() / 500) + "px;\n" \
                      "border-radius: " + str(btnSizeCir.x() / 2) + "px;\n" \
                      "}"

        btnStyleCor = "QPushButton{\n" \
                      "border-style: solid;\n" \
                      "border-color: black;\n" \
                      "border-width: " + str(self.screen.y() / 500) + "px;\n" \
                      "border-radius: 0px;\n" \
                      "}"
        
	# Create and place objects
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QRect(border.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton.setStyleSheet(btnStyleCir)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.addChar(self.pushButton.text()))
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_2.setStyleSheet(btnStyleCir)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.addChar(self.pushButton_2.text()))
        
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_3.setStyleSheet(btnStyleCir)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.addChar(self.pushButton_3.text()))

        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_4.setStyleSheet(btnStyleCir)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda: self.addChar(self.pushButton_4.text()))
        
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QRect(border.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_5.setStyleSheet(btnStyleCir)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda: self.addChar(self.pushButton_5.text()))
        
        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_6.setStyleSheet(btnStyleCir)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(lambda: self.addChar(self.pushButton_6.text()))

        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setGeometry(QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_7.setStyleSheet(btnStyleCir)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(lambda: self.addChar(self.pushButton_7.text()))

        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.setGeometry(QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_8.setStyleSheet(btnStyleCir)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(lambda: self.addChar(self.pushButton_8.text()))

        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QRect(btnSizeCor.x(), 0, self.screen.x() - btnSizeCor.x()*2, btnSizeCor.y()))
        self.textBrowser.setObjectName("textBrowser")
        
        self.pushButton_9 = QtWidgets.QPushButton(self)
        self.pushButton_9.setGeometry(QRect(0, 0, btnSizeCor.x(), btnSizeCor.y()))
        self.pushButton_9.setStyleSheet(btnStyleCor)
        self.pushButton_9.clicked.connect(self.goBack)

        self.setWindowTitle("Eyetalk A-G")
        self.pushButton.setText(self.charList[0])
        self.pushButton_2.setText(self.charList[1])
        self.pushButton_3.setText(self.charList[2])
        self.pushButton_4.setText(self.charList[3])
        self.pushButton_5.setText(self.charList[4])
        self.pushButton_6.setText(self.charList[5])
        self.pushButton_7.setText(self.charList[6])
        self.pushButton_8.setText(self.charList[7])
        self.pushButton_9.setText("Back")

        QtCore.QMetaObject.connectSlotsByName(self)
        
    
