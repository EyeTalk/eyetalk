from ui.base_8_button import BaseEightButton
from ui.keyboard_constants import *

class EightButtonGreeting(BaseEightButton):
    def __init__(self, parent, detector):
        BaseEightButton.__init__(self, parent, detector)
        self.base_string = "Please select an option"

        self.set_button_texts()
        self.set_text_label(self.base_string)

    def goBack(self):
        self.parent.stacked_widget.setCurrentIndex(1)
        self.hide()

    def openWindow(self, num):
        self.parent.set_active_widget(num)

    def set_button_texts(self):
        self.setWindowTitle("EyeTalk")
        self.pushButton_1.setText(GREETINGS[0])
        self.pushButton_2.setText(GREETINGS[1])
        self.pushButton_3.setText(GREETINGS[2])
        self.pushButton_4.setText(GREETINGS[3])
        self.pushButton_5.setText(GREETINGS[4])
        self.pushButton_6.setText(GREETINGS[5])
        self.pushButton_7.setText(GREETINGS[6])
        self.pushButton_8.setText(GREETINGS[7])
        self.topLeftButton.setText(MAINMENU)

    def push_button_1_onclick(self):
        self.set_text_label(GREETINGS[0])

    def push_button_2_onclick(self):
        self.set_text_label(GREETINGS[1])

    def push_button_3_onclick(self):
        self.set_text_label(GREETINGS[2])

    def push_button_4_onclick(self):
        self.set_text_label(GREETINGS[3])

    def push_button_5_onclick(self):
        self.set_text_label(GREETINGS[4])

    def push_button_6_onclick(self):
        self.set_text_label(GREETINGS[5])

    def push_button_7_onclick(self):
        self.set_text_label(GREETINGS[6])

    def push_button_8_onclick(self):
        self.set_text_label(GREETINGS[7])

    def top_left_button_onclick(self):
        self.goBack()