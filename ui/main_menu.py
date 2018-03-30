import pygame
from ui.base_8_button import BaseEightButton
import ui.jokes


class EightButtonMainMenu(BaseEightButton):
    TEXT = 'text'
    READ = 'read'
    TEXT_LABEL = 'Say out loud\n\n>Send text<'
    READ_LABEL = '>Say out loud<\n\nSend text'

    def __init__(self, parent, detector):
        BaseEightButton.__init__(self, parent, detector)
        self.base_string = "Please select an option"

        self.set_button_texts()
        self.set_text_label(self.base_string)

        self.output_type = self.READ
        self.parent.output_method = self.READ

        pygame.init()

    def closeApp(self):
        self.set_inactive()
        self.close()
        self.parent.close()

    def openWindow(self, num):
        self.go_to_widget(num)

    def set_button_texts(self):
        self.setWindowTitle("EyeTalk")
        self.pushButton_1.setText("Yes / No")
        self.pushButton_2.setText("I feel...")
        self.pushButton_3.setText("I would\nlike to go...")
        self.pushButton_4.setText("Bell")
        self.pushButton_5.setText("Greetings")
        self.pushButton_6.setText("Entertainment")
        self.pushButton_7.setText("Tell Joke")
        self.pushButton_8.setText("Keyboard")
        self.topLeftButton.setText("Exit")
        self.topRightButton.setText(self.READ_LABEL)

    def push_button_1_onclick(self):
        self.openWindow(3)

    def push_button_2_onclick(self):
        self.openWindow(5)

    def push_button_3_onclick(self):
        self.openWindow(6)

    def push_button_4_onclick(self):
        pygame.mixer.music.load("ui/sounds/bell.mp3")
        pygame.mixer.music.play()

    def push_button_5_onclick(self):
        self.openWindow(4)

    def push_button_6_onclick(self):
        self.openWindow(7)

    def push_button_7_onclick(self):
        joke = ui.jokes.getJoke()
        while len(joke) > 280:
            joke = ui.jokes.getJoke()
        self.parent.handle_output(joke)

    def push_button_8_onclick(self):
        self.openWindow(2)

    def top_left_button_onclick(self):
        self.closeApp()

    def top_right_button_onclick(self):
        if self.output_type == self.TEXT:
            self.output_type = self.READ
            self.topRightButton.setText(self.READ_LABEL)
        else:
            self.output_type = self.TEXT
            self.topRightButton.setText(self.TEXT_LABEL)

        self.parent.output_method = self.output_type
