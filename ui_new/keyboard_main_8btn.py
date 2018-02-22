from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QPushButton,
QDesktopWidget, QStackedWidget)
from PyQt5.QtCore import pyqtSlot, QPointF, QRect, Qt
from add_char_8btn import EightBtnAddChar
from ui_layout import build_layout_dictionary, build_layout_element


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
        self.topRightButton = build_layout_element(self, layout_dict, 'topRightButton')
        self.textBrowser = build_layout_element(self, layout_dict, 'textBrowser')

        self.pushButton_4.clicked.connect(lambda: self.openWindow(3))
        self.pushButton_5.clicked.connect(lambda: self.openWindow(4))
        self.pushButton_6.clicked.connect(lambda: self.openWindow(5))
        self.pushButton_7.clicked.connect(lambda: self.openWindow(6))
        self.pushButton_8.clicked.connect(lambda: self.openWindow(7))
        

        self.textBrowser.setText(self.userStr)

        self.topLeftButton.clicked.connect(self.goBack)

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
        self.topLeftButton.setText("Exit")
        self.topRightButton.setText("Confirm")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    parent = QWidget()
    w = EightBtnKeyboardMain(parent)
    w.show()
    sys.exit(app.exec_())
