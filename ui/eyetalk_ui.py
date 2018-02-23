from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QStackedWidget
from PyQt5.QtCore import QPointF

from ui.calibration import Calibration
from ui.main_menu import EightButtonMainMenu
from ui.keyboard import EightButtonKeyboard

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
        self.stacked_widget.setCurrentIndex(1)

