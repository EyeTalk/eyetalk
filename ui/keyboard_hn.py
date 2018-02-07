from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QPointF, QRect

class Ui_hn(object):
    def __init__(self, parent):
        self.parent = parent
        
    def openWindow(self, next_win, cur_win):
        if next_win == "main":
            self.parent.show()
        cur_win.hide()

    def addChar(self, char, cur_win):
        textBrowser = self.parent.findChild(QtWidgets.QTextBrowser)
        if char == "Backspace":
            textBrowser.setText(textBrowser.toPlainText()[:-1])
        else:
            textBrowser.setText(textBrowser.toPlainText() + char)
        self.parent.show()
        cur_win.hide()
    
    def setupUi(self, OtherWindow):
        OtherWindow.setObjectName("OtherWindow")
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        self.screen = QPointF(sg.width(), sg.height())
        OtherWindow.resize(self.screen.x(), self.screen.y())

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
        self.pushButton = QtWidgets.QPushButton(OtherWindow)
        self.pushButton.setGeometry(QRect(border.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton.setStyleSheet(btnStyleCir)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.addChar(self.pushButton.text(), OtherWindow))
        
        self.pushButton_2 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_2.setGeometry(QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_2.setStyleSheet(btnStyleCir)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.addChar(self.pushButton_2.text(), OtherWindow))
        
        self.pushButton_3 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_3.setGeometry(QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_3.setStyleSheet(btnStyleCir)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.addChar(self.pushButton_3.text(), OtherWindow))

        self.pushButton_4 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_4.setGeometry(QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_4.setStyleSheet(btnStyleCir)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda: self.addChar(self.pushButton_4.text(), OtherWindow))
        
        self.pushButton_5 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_5.setGeometry(QRect(border.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_5.setStyleSheet(btnStyleCir)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda: self.addChar(self.pushButton_5.text(), OtherWindow))
        
        self.pushButton_6 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_6.setGeometry(QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_6.setStyleSheet(btnStyleCir)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(lambda: self.addChar(self.pushButton_6.text(), OtherWindow))

        self.pushButton_7 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_7.setGeometry(QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_7.setStyleSheet(btnStyleCir)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(lambda: self.addChar(self.pushButton_7.text(), OtherWindow))

        self.pushButton_8 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_8.setGeometry(QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_8.setStyleSheet(btnStyleCir)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(lambda: self.addChar(self.pushButton_8.text(), OtherWindow))

        self.textBrowser = QtWidgets.QTextBrowser(OtherWindow)
        self.textBrowser.setGeometry(QRect(btnSizeCor.x(), 0, self.screen.x() - btnSizeCor.x()*2, btnSizeCor.y()))
        self.textBrowser.setObjectName("textBrowser")
        
        self.pushButton_9 = QtWidgets.QPushButton(OtherWindow)
        self.pushButton_9.setGeometry(QRect(0, 0, btnSizeCor.x(), btnSizeCor.y()))
        self.pushButton_9.setStyleSheet(btnStyleCor)
        self.pushButton_9.clicked.connect(lambda: self.openWindow("main", OtherWindow))

        self.retranslateUi(OtherWindow)
        QtCore.QMetaObject.connectSlotsByName(OtherWindow)

    def retranslateUi(self, OtherWindow):
        _translate = QtCore.QCoreApplication.translate
        OtherWindow.setWindowTitle("EyeTalk H-N")
        self.pushButton.setText("H")
        self.pushButton_2.setText("I")
        self.pushButton_3.setText("J")
        self.pushButton_4.setText("K")
        self.pushButton_5.setText("L")
        self.pushButton_6.setText("M")
        self.pushButton_7.setText("N")
        self.pushButton_8.setText("Backspace")
        self.pushButton_9.setText("Back")
