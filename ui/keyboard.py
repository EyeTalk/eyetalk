from ui.base_8_button import BaseEightButton
from ui.keyboard_constants import *
from ui.word_recommendations.recommendations import RecommendationSystem
from ui.tts import *


class EightButtonKeyboard(BaseEightButton):

    def __init__(self, parent, detector):
        BaseEightButton.__init__(self, parent, detector)

        self.label_text = ''

        self.text_1 = ''
        self.text_2 = ''
        self.text_3 = ''
        self.text_4 = ''
        self.text_5 = ''
        self.text_6 = ''
        self.text_7 = ''
        self.text_8 = ''

        self.topLeftButton.setText(MAINMENU)
        self.topRightButton.setText(CONFIRM)

        self.rec = RecommendationSystem()

        self.current_keyboard_screen = 0

        self.load_keyboard_screen(0)

    def goBack(self):
        self.go_to_widget(1)
        self.hide()

    def openWindow(self, num):
        self.hide()
        self.go_to_widget(num)

    def load_keyboard_screen(self, keyboard_index):
        layout = TEXT_LAYOUTS[keyboard_index]

        self.text_1 = layout[0]
        self.text_2 = layout[1]
        self.text_3 = layout[2]
        self.text_4 = layout[3]
        self.text_5 = layout[4]
        self.text_6 = layout[5]
        self.text_7 = layout[6]
        self.text_8 = layout[7]

        if keyboard_index == 0:
            self.pushButton_1.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            self.pushButton_3.setDisabled(True)
            wordList = self.rec.get_recommendation(self.label_text)
            if len(wordList) > 0:
                self.text_1 = wordList[0].upper()
                self.pushButton_1.setEnabled(True)
            if len(wordList) > 1:
                self.text_2 = wordList[1].upper()
                self.pushButton_2.setEnabled(True)
            if len(wordList) > 2:
                self.text_3 = wordList[2].upper()
                self.pushButton_3.setEnabled(True)
        else:
            self.pushButton_1.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)

        self.pushButton_1.setText(self.text_1)
        self.pushButton_2.setText(self.text_2)
        self.pushButton_3.setText(self.text_3)
        self.pushButton_4.setText(self.text_4)
        self.pushButton_5.setText(self.text_5)
        self.pushButton_6.setText(self.text_6)
        self.pushButton_7.setText(self.text_7)
        self.pushButton_8.setText(self.text_8)

        if keyboard_index > 0:
            self.topLeftButton.setText(BACK)

        self.current_keyboard_screen = keyboard_index

    def add_character(self, text_char):
        self.label_text += text_char
        self.set_text_label(self.label_text)
        self.topLeftButton.setText(CLEAR)

    def delete_last_char(self):
        self.label_text = self.label_text[:-1]
        self.set_text_label(self.label_text)
        if (self.label_text == ""):
            self.topLeftButton.setText(MAINMENU)

    def add_predicted(self, text_word):
        space_index = self.label_text.rfind(' ')
        if space_index > 0:
            self.label_text = self.label_text[:space_index+1]
            self.label_text += text_word
            self.set_text_label(self.label_text)
        else:
            self.label_text = text_word
            self.set_text_label(text_word)
            self.topLeftButton.setText(CLEAR)

    def clear_all(self):
        self.label_text = ''
        self.set_text_label(self.label_text)

    def push_button_1_onclick(self):
        if self.pushButton_1.isEnabled():
            if self.current_keyboard_screen == 0:
                self.add_predicted(self.text_1 + ' ')
                self.load_keyboard_screen(0)
            elif self.current_keyboard_screen == 6:
                self.load_keyboard_screen(5)
            else:
                self.add_character(self.text_1)
                self.load_keyboard_screen(0)

    def push_button_2_onclick(self):
        if self.pushButton_2.isEnabled():
            if self.current_keyboard_screen == 0:
                self.add_predicted(self.text_2 + ' ')
                self.load_keyboard_screen(0)
            else:
                self.add_character(self.text_2)
                self.load_keyboard_screen(0)

    def push_button_3_onclick(self):
        if self.pushButton_3.isEnabled():
            if self.current_keyboard_screen == 0:
                self.add_predicted(self.text_3 + ' ')
                self.load_keyboard_screen(0)
            else:
                self.add_character(self.text_3)
                self.load_keyboard_screen(0)

    def push_button_4_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(5)
        else:
            self.add_character(self.text_4)
            self.load_keyboard_screen(0)

    def push_button_5_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(1)
        else:
            self.add_character(self.text_5)
            self.load_keyboard_screen(0)

    def push_button_6_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(2)
        else:
            self.add_character(self.text_6)
            self.load_keyboard_screen(0)

    def push_button_7_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(3)
        else:
            self.add_character(self.text_7)
            self.load_keyboard_screen(0)

    def push_button_8_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(4)
        elif self.current_keyboard_screen == 1:
            self.add_character(' ')
            self.load_keyboard_screen(0)
        elif self.current_keyboard_screen == 2:
            self.delete_last_char()
            self.load_keyboard_screen(0)
        elif self.current_keyboard_screen == 5:
            self.load_keyboard_screen(6)
        else:
            self.add_character(self.text_8)
            self.load_keyboard_screen(0)

    def top_left_button_onclick(self):
        if self.current_keyboard_screen == 0:
            if self.label_text:
                self.clear_all()
                self.load_keyboard_screen(0)
                self.topLeftButton.setText(MAINMENU)
            else:
                self.clear_all()
                self.goBack()
        else:
            if self.label_text:
                self.topLeftButton.setText(CLEAR)
            else:
                self.topLeftButton.setText(MAINMENU)
            self.load_keyboard_screen(0)

    def top_right_button_onclick(self):
        textToSpeech(self.label_text)
        self.clear_all()
        self.topLeftButton.setText(MAINMENU)
        self.load_keyboard_screen(0)
