from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QPushButton, QDesktopWidget
from PyQt5.QtCore import pyqtSlot, QPointF, QRect, Qt
from keyboard_ag import Ui_ag
from keyboard_hn import Ui_hn
from keyboard_ou import Ui_ou
from keyboard_vz import Ui_vz

class Ui_MainWindow(object):
    def openWindow(self, next_win, cur_win):
        if next_win == "ag":
            self.agWidget.showFullScreen()
        elif next_win == "hn":
            self.hnWidget.showFullScreen()
        elif next_win == "ou":
            self.ouWidget.showFullScreen()
        elif next_win == "vz":
            self.vzWidget.showFullScreen()
        #cur_win.hide()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        self.screen = QPointF(sg.width(), sg.height())
        MainWindow.resize(self.screen.x(), self.screen.y())

        # Setup UIs for each letter range
        self.agWidget = QtWidgets.QWidget()
        self.ag = Ui_ag(MainWindow)
        self.ag.setupUi(self.agWidget)
        self.hnWidget = QtWidgets.QWidget()
        self.hn = Ui_hn(MainWindow)
        self.hn.setupUi(self.hnWidget)
        self.ouWidget = QtWidgets.QWidget()
        self.ou = Ui_ou(MainWindow)
        self.ou.setupUi(self.ouWidget)
        self.vzWidget = QtWidgets.QWidget()
        self.vz = Ui_vz(MainWindow)
        self.vz.setupUi(self.vzWidget)

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
        self.pushButton = QtWidgets.QPushButton(MainWindow)
        self.pushButton.setGeometry(QRect(border.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton.setStyleSheet(btnStyleCir)
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton_2 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_2.setStyleSheet(btnStyleCir)
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.pushButton_3 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_3.setStyleSheet(btnStyleCir)
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.pushButton_4 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y()*2 - btnSizeCir.y()*2, btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_4.setStyleSheet(btnStyleCir)
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.pushButton_5 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_5.setGeometry(QtCore.QRect(border.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_5.setStyleSheet(btnStyleCir)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda: self.openWindow("ag", MainWindow))

        self.pushButton_6 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_6.setGeometry(QtCore.QRect(border.x()*2 + btnSizeCir.x(), self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_6.setStyleSheet(btnStyleCir)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(lambda: self.openWindow("hn", MainWindow))
        
        self.pushButton_7 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_7.setGeometry(QtCore.QRect(border.x()*3 + btnSizeCir.x()*2, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_7.setStyleSheet(btnStyleCir)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(lambda: self.openWindow("ou", MainWindow))
        
        self.pushButton_8 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_8.setGeometry(QtCore.QRect(border.x()*4 + btnSizeCir.x()*3, self.screen.y() - border.y() - btnSizeCir.y(), btnSizeCir.x(), btnSizeCir.y()))
        self.pushButton_8.setStyleSheet(btnStyleCir)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(lambda: self.openWindow("vz", MainWindow))
        
        self.textBrowser = QtWidgets.QTextBrowser(MainWindow)
        self.textBrowser.setGeometry(QtCore.QRect(btnSizeCor.x(), 0, self.screen.x() - btnSizeCor.x()*2, btnSizeCor.y()))
        self.textBrowser.setText(self.userStr)
        self.textBrowser.setObjectName("textBrowser")
        
        self.pushButton_9 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_9.setGeometry(QtCore.QRect(0, 0, btnSizeCor.x(), btnSizeCor.y()))
        self.pushButton_9.setStyleSheet(btnStyleCor)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(MainWindow.close)
        
        self.pushButton_10 = QtWidgets.QPushButton(MainWindow)
        self.pushButton_10.setGeometry(QtCore.QRect(self.screen.x() - btnSizeCor.x(), 0, btnSizeCor.x(), btnSizeCor.y()))
        self.pushButton_10.setStyleSheet(btnStyleCor)
        self.pushButton_10.setObjectName("pushButton_10")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("EyeTalk")
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
    keyboard_main = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(keyboard_main)
    keyboard_main.showFullScreen()
    sys.exit(app.exec_())
