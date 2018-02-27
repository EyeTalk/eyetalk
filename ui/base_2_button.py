from numpy import argmax

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMetaObject, QTimer

from ui.ui_layout import build_layout_dictionary, build_layout_element


class BaseTwoButton(QWidget):

    def __init__(self, parent, detector):
        QMainWindow.__init__(self)
        self.parent = parent
        self.detector = detector

        self.is_active = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_gaze)

        self.pushButton_1 = None
        self.pushButton_2 = None
        self.topLeftButton = None
        self.topRightButton = None
        self.textLabel = None

        self.text_string = ""
        self.last_id = -1

        self.setupUi()

    def set_active(self):
        self.is_active = True
        self.timer.start(10)

    def check_gaze(self):
        given_id, probabilities = self.detector.sample()
        label = argmax(probabilities)

        print(given_id, label)

        if given_id != self.last_id:
            self.last_id = given_id
            print(label)
            # self.show_gazed_button(label)

    def go_to_widget(self, widget_number):
        self.timer.stop()
        self.parent.set_active_widget(widget_number)

    def setupUi(self):
        self.setWindowTitle("EyeTalk")

        sg = QDesktopWidget().screenGeometry()

        layout_dict = build_layout_dictionary(sg.width(), sg.height())

        # Create and place objects
        self.pushButton_1 = build_layout_element(self, layout_dict, 'pushButton_1_big', 2)
        self.pushButton_2 = build_layout_element(self, layout_dict, 'pushButton_2_big', 2)
        self.topLeftButton = build_layout_element(self, layout_dict, 'topLeftButton', 2)
        self.topRightButton = build_layout_element(self, layout_dict, 'topRightButton', 2)
        self.textLabel = build_layout_element(self, layout_dict, 'textLabel', 2)

        QMetaObject.connectSlotsByName(self)

        self.pushButton_1.clicked.connect(self.push_button_1_onclick)
        self.pushButton_2.clicked.connect(self.push_button_2_onclick)
        self.topLeftButton.clicked.connect(self.top_left_button_onclick)
        self.topRightButton.clicked.connect(self.top_right_button_onclick)
        self.textLabel.setWordWrap(True)

    def set_text_label(self, text):
        self.text_string = text
        self.textLabel.setText(text)

    def show_gazed_button(self, button_id):

        self.pushButton_1.setStyleSheet('background-color: red')

    """
    Simply override any of these methods in a subclass to implement a click handler
    """

    def push_button_1_onclick(self):
        pass

    def push_button_2_onclick(self):
        pass

    def top_left_button_onclick(self):
        pass

    def top_right_button_onclick(self):
        pass
