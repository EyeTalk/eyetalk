import pyglet
from ui.base_8_button import BaseEightButton


class EightButtonMainMenu(BaseEightButton):
    def __init__(self, parent, detector):
        BaseEightButton.__init__(self, parent, detector)
        self.base_string = "Please select an option"

        self.set_button_texts()
        self.set_text_label(self.base_string)

    def closeApp(self):
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
        self.pushButton_7.setText("Games")
        self.pushButton_8.setText("Keyboard")
        self.topLeftButton.setText("Exit")

    def push_button_1_onclick(self):
        self.openWindow(3)

    def push_button_2_onclick(self):
        self.openWindow(5)

    def push_button_3_onclick(self):
        self.openWindow(6)

    def push_button_4_onclick(self):
        bell = pyglet.media.load("ui/sounds/bell.mp3", streaming=False)
        bell.play()

    def push_button_5_onclick(self):
        self.openWindow(4)

    def push_button_8_onclick(self):
        self.openWindow(2)

    def top_left_button_onclick(self):
        self.closeApp()
