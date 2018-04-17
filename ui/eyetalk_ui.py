import ui.output_text
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QStackedWidget
from PyQt5.QtCore import QPointF

from ui.calibration import Calibration
from ui.main_menu import EightButtonMainMenu
from ui.keyboard import EightButtonKeyboard
from ui.yes_no import TwoButtonYesNo
from ui.greetings import EightButtonGreeting
from ui.feelings import EightButtonFeeling
from ui.go import TwoButtonGo
from ui.entertainment import EightButtonEntertainment
from ui.exit import TwoButtonExit

from backend.GazeDetector import GazeDetector


class MainUIWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        sg = QDesktopWidget().screenGeometry()

        self.showFullScreen()
        self.detector = GazeDetector(load_model=True)

        self.screen = QPointF(sg.width(), sg.height())

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(Calibration(self, self.detector))
        self.stacked_widget.addWidget(EightButtonMainMenu(self, self.detector))
        self.stacked_widget.addWidget(EightButtonKeyboard(self, self.detector))
        self.stacked_widget.addWidget(TwoButtonYesNo(self, self.detector))
        self.stacked_widget.addWidget(EightButtonGreeting(self, self.detector))
        self.stacked_widget.addWidget(EightButtonFeeling(self, self.detector))
        self.stacked_widget.addWidget(TwoButtonGo(self, self.detector))
        self.stacked_widget.addWidget(EightButtonEntertainment(self, self.detector))
        self.stacked_widget.addWidget(TwoButtonExit(self, self.detector))
        self.set_active_widget(0)

        self.output_method = None

    def set_active_widget(self, widget_number):
        self.stacked_widget.setCurrentIndex(widget_number)
        self.stacked_widget.widget(widget_number).set_active()

    def handle_output(self, message):
        if message:
            if self.output_method == 'text':
                ui.output_text.send_text_message(message)
                ui.output_text.textToSpeech('Message sent.')
            else:
                ui.output_text.textToSpeech(message)
