from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QWidget
from PyQt5.QtCore import QMetaObject
from PyQt5.QtCore import Qt

from ui.ui_layout import build_layout_dictionary, build_layout_element


class BaseEightButton(QWidget):

    def __init__(self, parent):
        QMainWindow.__init__(self)
        self.parent = parent

        self.pushButton_1 = None
        self.pushButton_2 = None
        self.pushButton_3 = None
        self.pushButton_4 = None
        self.pushButton_5 = None
        self.pushButton_6 = None
        self.pushButton_7 = None
        self.pushButton_8 = None
        self.topLeftButton = None
        self.topRightButton = None
        self.textLabel = None

        self.text_string = ""

        self.setupUi()

    def go_to_widget(self, widget_number):
        self.parent.stacked_widget.setCurrentIndex(widget_number)

    def setupUi(self):
        self.setWindowTitle("EyeTalk")

        sg = QDesktopWidget().screenGeometry()

        layout_dict = build_layout_dictionary(sg.width(), sg.height())

        # Create and place objects
        self.pushButton_1 = build_layout_element(self, layout_dict, 'pushButton_1')
        self.pushButton_2 = build_layout_element(self, layout_dict, 'pushButton_2')
        self.pushButton_3 = build_layout_element(self, layout_dict, 'pushButton_3')
        self.pushButton_4 = build_layout_element(self, layout_dict, 'pushButton_4')
        self.pushButton_5 = build_layout_element(self, layout_dict, 'pushButton_5')
        self.pushButton_6 = build_layout_element(self, layout_dict, 'pushButton_6')
        self.pushButton_7 = build_layout_element(self, layout_dict, 'pushButton_7')
        self.pushButton_8 = build_layout_element(self, layout_dict, 'pushButton_8')
        self.topLeftButton = build_layout_element(self, layout_dict, 'topLeftButton')
        self.topRightButton = build_layout_element(self, layout_dict, 'topRightButton')
        self.textLabel = build_layout_element(self, layout_dict, 'textLabel')

        QMetaObject.connectSlotsByName(self)

        self.pushButton_1.clicked.connect(self.push_button_1_onclick)
        self.pushButton_2.clicked.connect(self.push_button_2_onclick)
        self.pushButton_3.clicked.connect(self.push_button_3_onclick)
        self.pushButton_4.clicked.connect(self.push_button_4_onclick)
        self.pushButton_5.clicked.connect(self.push_button_5_onclick)
        self.pushButton_6.clicked.connect(self.push_button_6_onclick)
        self.pushButton_7.clicked.connect(self.push_button_7_onclick)
        self.pushButton_8.clicked.connect(self.push_button_8_onclick)
        self.topLeftButton.clicked.connect(self.top_left_button_onclick)
        self.topRightButton.clicked.connect(self.top_right_button_onclick)
        self.textLabel.setAlignment(Qt.AlignHCenter)

    def set_text_label(self, text):
        self.text_string = text
        self.textLabel.setText(text)

    """
    Simply override any of these methods in a subclass to implement a click handler
    """

    def push_button_1_onclick(self):
        pass

    def push_button_2_onclick(self):
        pass

    def push_button_3_onclick(self):
        pass

    def push_button_4_onclick(self):
        pass

    def push_button_5_onclick(self):
        pass

    def push_button_6_onclick(self):
        pass

    def push_button_7_onclick(self):
        pass

    def push_button_8_onclick(self):
        pass

    def top_left_button_onclick(self):
        pass

    def top_right_button_onclick(self):
        pass
