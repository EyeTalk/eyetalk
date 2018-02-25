from ui.base_2_button import BaseTwoButton
from ui.keyboard_constants import *

class TwoButtonYesNo(BaseTwoButton):
    def __init__(self, parent, detector):
        BaseTwoButton.__init__(self, parent, detector)
        self.base_string = "Please select an option"

        self.set_button_texts()
        self.set_text_label(self.base_string)

    def goBack(self):
        self.parent.stacked_widget.setCurrentIndex(1)
        self.hide()

    def openWindow(self, num):
        self.parent.set_active_widget(num)

    def set_button_texts(self):
        self.pushButton_1.setText(YES)
        self.pushButton_2.setText(NO)
        self.topLeftButton.setText(MAINMENU)

    def push_button_1_onclick(self):
        self.set_text_label(YES)

    def push_button_2_onclick(self):
        self.set_text_label(NO)

    def top_left_button_onclick(self):
        self.goBack()
