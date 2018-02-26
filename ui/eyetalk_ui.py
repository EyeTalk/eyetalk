from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QStackedWidget
from PyQt5.QtCore import QPointF

from ui.calibration import Calibration
from ui.main_menu import EightButtonMainMenu
from ui.keyboard import EightButtonKeyboard
from ui.yes_no import TwoButtonYesNo
from ui.greetings import EightButtonGreeting

from backend.GazeDetector import GazeDetector


class MainUIWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        sg = QDesktopWidget().screenGeometry()

        self.detector = GazeDetector()

        self.screen = QPointF(sg.width(), sg.height())
        self.showFullScreen()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(Calibration(self, self.detector))
        self.stacked_widget.addWidget(EightButtonMainMenu(self, self.detector))
        self.stacked_widget.addWidget(EightButtonKeyboard(self, self.detector))
        self.stacked_widget.addWidget(TwoButtonYesNo(self, self.detector))
        self.stacked_widget.addWidget(EightButtonGreeting(self, self.detector))
        self.set_active_widget(0)

    def set_active_widget(self, widget_number):
        self.stacked_widget.setCurrentIndex(widget_number)
        self.stacked_widget.widget(widget_number).set_active()

