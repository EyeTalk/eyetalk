from ui.base_8_button import BaseEightButton
from ui.keyboard_constants import *


class EightButtonFeeling(BaseEightButton):
    def __init__(self, parent, detector):
        BaseEightButton.__init__(self, parent, detector)
        self.base_string = "I feel "

        self.set_button_texts()
        self.set_text_label(self.base_string)

    def goBack(self):
        self.go_to_widget(1)
        self.hide()

    def openWindow(self, num):
        self.go_to_widget(num)

    def set_button_texts(self):
        self.setWindowTitle("EyeTalk")
        self.pushButton_1.setText(FEELINGS[0])
        self.pushButton_2.setText(FEELINGS[1])
        self.pushButton_3.setText(FEELINGS[2])
        self.pushButton_4.setText(FEELINGS[3])
        self.pushButton_5.setText(FEELINGS[4])
        self.pushButton_6.setText(FEELINGS[5])
        self.pushButton_7.setText(FEELINGS[6])
        self.pushButton_8.setText(FEELINGS[7])
        self.topLeftButton.setText(MAINMENU)

    def push_button_1_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[0].replace("-", ""))

    def push_button_2_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[1])

    def push_button_3_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[2])

    def push_button_4_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[3])

    def push_button_5_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[4])

    def push_button_6_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[5])

    def push_button_7_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[6])

    def push_button_8_onclick(self):
        self.parent.handle_output(self.base_string + FEELINGS[7])

    def top_left_button_onclick(self):
        self.goBack()
