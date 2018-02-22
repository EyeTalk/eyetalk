from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QPushButton,
QDesktopWidget, QStackedWidget)
from PyQt5.QtCore import pyqtSlot, QPointF, QRect, Qt
from add_char_8btn import EightBtnAddChar

from ui_layout import build_layout_dictionary, build_layout_element



class EightBtnMain(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.parent = parent
        self.setupUi()

    def closeApp(self):
        self.close()
        self.parent.close()

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

        layout_dict = build_layout_dictionary(sg.width(), sg.height())

        # Create and place objects
        self.pushButton = build_layout_element(self, layout_dict, 'pushButton_1')
        self.pushButton_2 = build_layout_element(self, layout_dict, 'pushButton_2')
        self.pushButton_3 = build_layout_element(self, layout_dict, 'pushButton_3')
        self.pushButton_4 = build_layout_element(self, layout_dict, 'pushButton_4')
        self.pushButton_5 = build_layout_element(self, layout_dict, 'pushButton_5')
        self.pushButton_6 = build_layout_element(self, layout_dict, 'pushButton_6')
        self.pushButton_7 = build_layout_element(self, layout_dict, 'pushButton_7')
        self.pushButton_8 = build_layout_element(self, layout_dict, 'pushButton_8')
        self.topLeftButton = build_layout_element(self, layout_dict, 'topLeftButton')
        # self.topRightButton = build_layout_element(self, layout_dict, 'topRightButton')
        self.textBrowser = build_layout_element(self, layout_dict, 'textBrowser')

        self.pushButton_8.clicked.connect(lambda: self.openWindow(2))
        self.topLeftButton.clicked.connect(self.closeApp)
        self.textBrowser.setText(self.userStr)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("EyeTalk")
        self.pushButton.setText("Yes / No")
        self.pushButton_2.setText("Body")
        self.pushButton_3.setText("Greetings")
        self.pushButton_4.setText("Bell")
        self.pushButton_5.setText("Jokes")
        self.pushButton_6.setText("Music")
        self.pushButton_7.setText("Games")
        self.pushButton_8.setText("Keyboard")
        self.topLeftButton.setText("Exit")

