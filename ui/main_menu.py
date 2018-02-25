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
        self.parent.set_active_widget(num)

    def set_button_texts(self):
        self.setWindowTitle("EyeTalk")
        self.pushButton_1.setText("Yes / No")
        self.pushButton_2.setText("Body")
        self.pushButton_3.setText("Greetings")
        self.pushButton_4.setText("Bell")
        self.pushButton_5.setText("Jokes")
        self.pushButton_6.setText("Music")
        self.pushButton_7.setText("Games")
        self.pushButton_8.setText("Keyboard")
        self.topLeftButton.setText("Exit")

    def push_button_1_onclick(self):
        self.openWindow(3)

    def push_button_8_onclick(self):
        self.openWindow(2)

    def top_left_button_onclick(self):
        self.closeApp()
