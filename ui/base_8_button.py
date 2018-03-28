from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QWidget
from PyQt5.QtCore import QMetaObject, QTimer

from ui.ui_layout import build_layout_dictionary, build_layout_element
from ui.eye_state_manager import EyeStateManager


class BaseEightButton(QWidget):

    def __init__(self, parent, detector):
        QMainWindow.__init__(self)
        self.parent = parent
        self.detector = detector
        self.eye_state_manager = EyeStateManager()

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

        # TODO: Implement function to map probabilities to button

        self.layout_dict = None

        self.text_string = ""

        self.setupUi()

    def set_active(self):
        self.is_active = True

        def start_timer():
            self.timer.start(10)

        QTimer.singleShot(250, start_timer)
        self.eye_state_manager = EyeStateManager()

    def set_inactive(self):
        self.is_active = False
        self.show_gazed_button(-1)
        self.timer.stop()

    def check_gaze(self):
        given_id, blink, probabilities = self.detector.sample()

        self.eye_state_manager.handle_input(given_id, blink, probabilities)

        if self.eye_state_manager.selection_made:
            self.push_button(self.eye_state_manager.selected_label)
            # TODO: Add noise here?
        elif self.eye_state_manager.new_gazed_button:
            self.show_gazed_button(self.eye_state_manager.selected_label)

    def go_to_widget(self, widget_number):
        self.set_inactive()
        self.show_gazed_button(-1)
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

    def push_button(self, button):
        callbacks = {
            1: self.push_button_1_onclick,
            2: self.push_button_2_onclick,
            3: self.push_button_3_onclick,
            4: self.push_button_4_onclick,
            5: self.push_button_5_onclick,
            6: self.push_button_6_onclick,
            7: self.push_button_7_onclick,
            8: self.push_button_8_onclick,
            9: self.top_left_button_onclick,
            10: self.top_right_button_onclick
        }

        button_function = callbacks.get(button, None)
        if button_function is not None:
            button_function()

        def restart_timer():
            if self.is_active:
                self.set_active()

        self.timer.stop()
        QTimer.singleShot(500, restart_timer)

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
