from ui.base_2_button import BaseTwoButton
from ui.keyboard_constants import *
from ui.tts import *

class TwoButtonGo(BaseTwoButton):
    def __init__(self, parent, detector):
        BaseTwoButton.__init__(self, parent, detector)
        self.base_string = "I would like to go "

        self.set_button_texts()
        self.set_text_label(self.base_string)

    def goBack(self):
        self.go_to_widget(1)
        self.hide()

    def openWindow(self, num):
        self.go_to_widget(num)

    def set_button_texts(self):
        self.pushButton_1.setText(OUTSIDE)
        self.pushButton_2.setText(HOME)
        self.topLeftButton.setText(MAINMENU)

    def push_button_1_onclick(self):
        textToSpeech(self.base_string + OUTSIDE)

    def push_button_2_onclick(self):
        textToSpeech(self.base_string + HOME)

    def top_left_button_onclick(self):
        self.goBack()
