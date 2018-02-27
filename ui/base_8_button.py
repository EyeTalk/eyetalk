import numpy as np
from queue import deque

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMetaObject, QTimer

from ui.ui_layout import build_layout_dictionary, build_layout_element


class BaseEightButton(QWidget):

    def __init__(self, parent, detector):
        QMainWindow.__init__(self)
        self.parent = parent
        self.detector = detector

        self.is_active = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_gaze)

        self.pushButton_1 = None
        self.pushButton_2 = None
        self.pushButton_3 = None
        self.pushButton_4 = None
        self.pushButton_5 = None
        self.pushButton_6 = None
        self.pushButton_7 = None
        self.pushButton_8 = None
        self.topLeftButton = None
        self.topRightButton = None
        self.textLabel = None

        self.layout_dict = None

        self.text_string = ""
        self.last_id = -1
        self.sample_queue = deque(maxlen=6)

        self.setupUi()

    def set_active(self):
        self.is_active = True
        self.timer.start(10)

    def get_average_label(self):
        all_data = np.concatenate(tuple(self.sample_queue), axis=0)
        averages = np.average(all_data, 0)
        return np.argmax(averages)

    def check_gaze(self):
        given_id, probabilities = self.detector.sample()

        if given_id != self.last_id:
            self.sample_queue.appendleft(probabilities)
            label = self.get_average_label()

            self.last_id = given_id
            self.show_gazed_button(label)

    def go_to_widget(self, widget_number):
        self.timer.stop()
        self.parent.set_active_widget(widget_number)

    def setupUi(self):
        self.setWindowTitle("EyeTalk")

        sg = QDesktopWidget().screenGeometry()

        self.layout_dict = build_layout_dictionary(sg.width(), sg.height())

        # Create and place objects
        self.pushButton_1 = build_layout_element(self, self.layout_dict, 'pushButton_1')
        self.pushButton_2 = build_layout_element(self, self.layout_dict, 'pushButton_2')
        self.pushButton_3 = build_layout_element(self, self.layout_dict, 'pushButton_3')
        self.pushButton_4 = build_layout_element(self, self.layout_dict, 'pushButton_4')
        self.pushButton_5 = build_layout_element(self, self.layout_dict, 'pushButton_5')
        self.pushButton_6 = build_layout_element(self, self.layout_dict, 'pushButton_6')
        self.pushButton_7 = build_layout_element(self, self.layout_dict, 'pushButton_7')
        self.pushButton_8 = build_layout_element(self, self.layout_dict, 'pushButton_8')
        self.topLeftButton = build_layout_element(self, self.layout_dict, 'topLeftButton')
        self.topRightButton = build_layout_element(self, self.layout_dict, 'topRightButton')
        self.textLabel = build_layout_element(self, self.layout_dict, 'textLabel')

        QMetaObject.connectSlotsByName(self)

        self.pushButton_1.clicked.connect(self.push_button_1_onclick)
        self.pushButton_2.clicked.connect(self.push_button_2_onclick)
        self.pushButton_3.clicked.connect(self.push_button_3_onclick)
        self.pushButton_4.clicked.connect(self.push_button_4_onclick)
        self.pushButton_5.clicked.connect(self.push_button_5_onclick)
        self.pushButton_6.clicked.connect(self.push_button_6_onclick)
        self.pushButton_7.clicked.connect(self.push_button_7_onclick)
        self.pushButton_8.clicked.connect(self.push_button_8_onclick)
        self.topLeftButton.clicked.connect(self.top_left_button_onclick)
        self.topRightButton.clicked.connect(self.top_right_button_onclick)
        self.textLabel.setWordWrap(True)

    def set_text_label(self, text):
        self.text_string = text
        self.textLabel.setText(text)

    def get_gazed_button_stylesheet(self, button_name, gazed_button):
        style_sheet = self.layout_dict['circle_stylesheet']
        label = self.layout_dict['eight_button_elements'][button_name]['label']

        if label == gazed_button:
            bg_color_loc = style_sheet.find('qlineargradient')
            bg_color_end = style_sheet.find(';')
            string = style_sheet[bg_color_loc:bg_color_end]
            return style_sheet.replace(string, 'red')
        else:
            return style_sheet

    def show_gazed_button(self, button_id):

        self.pushButton_1.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_1', button_id))
        self.pushButton_2.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_2', button_id))
        self.pushButton_3.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_3', button_id))
        self.pushButton_4.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_4', button_id))
        self.pushButton_5.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_5', button_id))
        self.pushButton_6.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_6', button_id))
        self.pushButton_7.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_7', button_id))
        self.pushButton_8.setStyleSheet(self.get_gazed_button_stylesheet('pushButton_8', button_id))
        self.topLeftButton.setStyleSheet(self.get_gazed_button_stylesheet('topLeftButton', button_id))
        self.topRightButton.setStyleSheet(self.get_gazed_button_stylesheet('topRightButton', button_id))


    """
    Simply override any of these methods in a subclass to implement a click handler
    """

    def push_button_1_onclick(self):
        pass

    def push_button_2_onclick(self):
        pass

    def push_button_3_onclick(self):
        pass

    def push_button_4_onclick(self):
        pass

    def push_button_5_onclick(self):
        pass

    def push_button_6_onclick(self):
        pass

    def push_button_7_onclick(self):
        pass

    def push_button_8_onclick(self):
        pass

    def top_left_button_onclick(self):
        pass

    def top_right_button_onclick(self):
        pass
