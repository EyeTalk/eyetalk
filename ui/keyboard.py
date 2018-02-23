from ui.base_8_button import BaseEightButton
from ui.keyboard_constants import *


class EightButtonKeyboard(BaseEightButton):

    def __init__(self, parent):
        BaseEightButton.__init__(self, parent)

        self.browser_text = ''

        self.text_1 = ''
        self.text_2 = ''
        self.text_3 = ''
        self.text_4 = ''
        self.text_5 = ''
        self.text_6 = ''
        self.text_7 = ''
        self.text_8 = ''

        self.topLeftButton.setText(EXIT)
        self.topRightButton.setText(CONFIRM)

        self.current_keyboard_screen = 0

        self.load_keyboard_screen(0)

    def goBack(self):
        self.parent.stacked_widget.setCurrentIndex(1)
        self.hide()

    def openWindow(self, num):
        self.hide()
        print(self.parent.stacked_widget.widget(num))
        self.parent.stacked_widget.setCurrentIndex(num)

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

        self.pushButton_1.setText(self.text_1)
        self.pushButton_2.setText(self.text_2)
        self.pushButton_3.setText(self.text_3)
        self.pushButton_4.setText(self.text_4)
        self.pushButton_5.setText(self.text_5)
        self.pushButton_6.setText(self.text_6)
        self.pushButton_7.setText(self.text_7)
        self.pushButton_8.setText(self.text_8)

        self.current_keyboard_screen = keyboard_index

    def add_character(self, text_char):
        self.browser_text += text_char
        self.set_text_browser(self.browser_text)

    def delete_last_char(self):
        self.browser_text = self.browser_text[:-1]
        self.set_text_browser(self.browser_text)

    def clear_all(self):
        self.browser_text = ''
        self.set_text_browser(self.browser_text)

    def push_button_1_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(1)
        else:
            self.add_character(self.text_1)
            self.load_keyboard_screen(0)

    def push_button_2_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(1)
        else:
            self.add_character(self.text_2)
            self.load_keyboard_screen(0)

    def push_button_3_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(1)
        else:
            self.add_character(self.text_3)
            self.load_keyboard_screen(0)

    def push_button_4_onclick(self):
        if self.current_keyboard_screen == 0:
            self.load_keyboard_screen(1)
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
        else:
            self.add_character(self.text_8)
            self.load_keyboard_screen(0)

    def top_left_button_onclick(self):
        if self.current_keyboard_screen == 0:
            if self.browser_text:
                self.clear_all()
                self.load_keyboard_screen(0)
                # self.topLeftButton.setText('Main Menu')
            else:
                self.clear_all()
                self.goBack()
        else:
            self.load_keyboard_screen(0)
