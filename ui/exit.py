from ui.base_2_button import BaseTwoButton
from ui.keyboard_constants import *


class TwoButtonExit(BaseTwoButton):
    def __init__(self, parent, detector):
        BaseTwoButton.__init__(self, parent, detector)
        self.base_string = "Are you sure you want to exit?"

        self.set_button_texts()
        self.set_text_label(self.base_string)

    def goBack(self):
        self.go_to_widget(1)
        self.hide()

    def openWindow(self, num):
        self.go_to_widget(num)

    def closeApp(self):
        self.set_inactive()
        self.close()
        self.parent.close()

    def set_button_texts(self):
        self.pushButton_1.setText(YES)
        self.pushButton_2.setText(NO)
        self.topLeftButton.setText(MAINMENU)

    def push_button_1_onclick(self):
        self.closeApp()

    def push_button_2_onclick(self):
        self.goBack()

    def top_left_button_onclick(self):
        self.goBack()
