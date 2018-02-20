from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QPushButton,
QDesktopWidget, QStackedWidget)
from PyQt5.QtCore import pyqtSlot, QPointF, QRect, Qt
from add_char_8btn import EightBtnAddChar

class EightBtnKeyboardMain(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.parent = parent
        self.setupUi()

    def goBack(self):
        self.parent.stacked_widget.setCurrentIndex(1)
        self.hide()

    def openWindow(self, num):
        self.hide()
        print(self.parent.stacked_widget.widget(num))
        self.parent.stacked_widget.setCurrentIndex(num)

    def setupUi(self):
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

        self.userStr = ""

        # Create and place objects
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QRect(border.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton.setStyleSheet(btnStyleCir)
        self.pushButton.setObjectName("pushButton_1")
        
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_2.setStyleSheet(btnStyleCir)
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_3.setStyleSheet(btnStyleCir)
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_4.setStyleSheet(btnStyleCir)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda: self.openWindow(3))
        
        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.setGeometry(QtCore.QRect(border.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_5.setStyleSheet(btnStyleCir)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda: self.openWindow(4))

        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.setGeometry(QtCore.QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_6.setStyleSheet(btnStyleCir)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(lambda: self.openWindow(5))
        
        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.setGeometry(QtCore.QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_7.setStyleSheet(btnStyleCir)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(lambda: self.openWindow(6))
        
        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.setGeometry(QtCore.QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_8.setStyleSheet(btnStyleCir)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(lambda: self.openWindow(7))
        
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(btnSizeCor.x(), 0, self.screen.x() - btnSizeCor.x()*2, btnSizeCor.y()))
        self.textBrowser.setText(self.userStr)
        self.textBrowser.setObjectName("textBrowser")
        
        self.pushButton_9 = QtWidgets.QPushButton(self)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 0, btnSizeCor.x(), btnSizeCor.y()))
        self.pushButton_9.setStyleSheet(btnStyleCor)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(self.goBack)
        
        self.pushButton_10 = QtWidgets.QPushButton(self)
        self.pushButton_10.setGeometry(QtCore.QRect(self.screen.x() - btnSizeCor.x(), 0, btnSizeCor.x(), btnSizeCor.y()))
        self.pushButton_10.setStyleSheet(btnStyleCor)
        self.pushButton_10.setObjectName("pushButton_10")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("EyeTalk")
        self.pushButton.setText("PredictedWord1")
        self.pushButton_2.setText("PredictedWord2")
        self.pushButton_3.setText("PredictedWord3")
        self.pushButton_4.setText("Numbers or Symbols")
        self.pushButton_5.setText("A B C D E F G\nSpace")
        self.pushButton_6.setText("H I J K L M N\nBackspace")
        self.pushButton_7.setText("O P Q R S T U\nCaps")
        self.pushButton_8.setText("V W X Y Z\n. ? !")
        self.pushButton_9.setText("Exit")
        self.pushButton_10.setText("Confirm")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    parent = QWidget()
    w = EightBtnKeyboardMain(parent)
    w.show()
    sys.exit(app.exec_())
