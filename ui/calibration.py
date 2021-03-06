from threading import Thread
from pymongo import MongoClient
from getpass import getuser
from random import gauss
from PyQt5.QtWidgets import (QGraphicsView,
        QGraphicsPixmapItem, QGraphicsScene, QDesktopWidget, QTextEdit, QLabel)
from PyQt5.QtGui import QPainter, QPixmap, QFont
from PyQt5.QtCore import (QObject, QPointF, QTimer, pyqtProperty, Qt)
from ui.ui_layout import build_layout_dictionary


EACH_BUTTON_TIME = 1800
PRE_CALIB_MSG_TIME = 8000


class Ball(QObject):
    def __init__(self):
        super().__init__()

        self.pixmap_item = QGraphicsPixmapItem(QPixmap("ui/red_ball.png"))

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class Calibration(QGraphicsView):
    def __init__(self, parent, detector, calibrate_now=True):
        super().__init__()

        self.parent = parent
        self.detector = detector

        self.is_active = False
        self.initView()
        self.data = []
        self.current_label = -1

        self.train_at_end = calibrate_now

    def set_active(self):
        self.is_active = True
        self.initSplashScreen()

    def initView(self):
        self.showFullScreen()

        self.sg = QDesktopWidget().screenGeometry()
        self.screen_width = self.sg.width()
        self.screen_height = self.sg.height()

        self.setWindowTitle("Calibration")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)

    def initSplashScreen(self):
        self.eye_image = QPixmap('ui/pupil.jpg')
        self.eye_image = self.eye_image.scaledToWidth(self.screen_width / 2)
        self.eye_image_item = QGraphicsPixmapItem(self.eye_image)
        x_loc = (self.screen_width - self.eye_image.width()) / 2
        y_loc = (self.screen_height - self.eye_image.height()) / 2
        self.eye_image_item.setPos(x_loc, y_loc)
        self.eye_image_item.setOpacity(0.50)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.screen_width, self.screen_height)
        self.scene.addItem(self.eye_image_item)

        self.label = QLabel()
        self.label.setText('EyeTalk')
        self.label.setFont(QFont("Arial", 200))
        self.label.adjustSize()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setAutoFillBackground(False)
        self.label.adjustSize()
        self.label.setStyleSheet("background-color: rgba(0,0,0,0%); color: #ef6c00;")
        self.label.move((self.screen_width - self.label.width()) / 2, (self.screen_height - self.label.height()) / 2)

        self.scene.addWidget(self.label)
        self.setScene(self.scene)

        QTimer.singleShot(4000, self.cleanSplashScreen)

    def cleanSplashScreen(self):
        self.scene.clear()
        del self.label
        del self.eye_image_item
        del self.eye_image
        self.initPreBallMessage()

    def initPreBallMessage(self):
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.calib_text = """
            <div>
                <h1>We will now begin Calibration</h1>
                <ul>
                    <li>Please stare at the red ball as it jumps around</li>
                    <li>This should last about 40 seconds total</li>
                    <li>The user interface will open when you finish</li>
                </ul>
                <h1>We will start in {secs} seconds</h1>
            </div>
            
        """
        self.seconds_left = int(PRE_CALIB_MSG_TIME / 1000)

        self.textbox.setHtml(self.calib_text.format(secs=self.seconds_left))
        self.textbox.setFrameStyle(0)

        self.textbox.show()
        self.textbox.setLineWrapMode(0)

        self.textbox.setMinimumWidth(self.textbox.document().size().width())
        self.textbox.setMinimumHeight(self.textbox.document().size().height())
        self.textbox.move((self.screen_width - self.textbox.width()) / 2,
                          (self.screen_height - self.textbox.height()) / 2)

        QTimer.singleShot(1000, self.update_countdown)

        QTimer.singleShot(PRE_CALIB_MSG_TIME, self.endPreBallMessage)

    def update_countdown(self):
        self.seconds_left -= 1
        self.textbox.setHtml(self.calib_text.format(secs=self.seconds_left))

        if self.seconds_left > 1:
            QTimer.singleShot(1000, self.update_countdown)

    def endPreBallMessage(self):
        self.textbox.deleteLater()
        self.textbox.hide()
        del self.textbox

        self.initBallAnimation()

    def initBallAnimation(self):
        self.ball = Ball()
        self.ball_width = self.ball.pixmap_item.boundingRect().size().width()
        self.ball_height = self.ball.pixmap_item.boundingRect().size().height()

        layout = build_layout_dictionary(self.screen_width,self.screen_height)
        elements = layout['eight_button_elements']

        self.pos = -1
        element_items = elements.items()
        self.button_positions = [QPointF(elem['top_left_x'] + elem['width'] / 2 - self.ball_width / 2,
                                         elem['top_left_y'] + elem['height'] / 2 - self.ball_height / 2)
                                 for _, elem in element_items]
        self.button_labels = [elem['label'] for _, elem in element_items]

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.screen_width, self.screen_height)
        self.scene.addItem(self.ball.pixmap_item)
        self.setScene(self.scene)

        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.move_ball)
        self.position_timer.start(EACH_BUTTON_TIME)

        self.sample_timer = QTimer(self)
        self.sample_timer.timeout.connect(self.sample_features)

        total_timeout = EACH_BUTTON_TIME * len(self.button_positions) * 2 + 1000
        QTimer.singleShot(total_timeout, self.endBallAnimation)
        self.move_ball()

    def move_ball(self):
        self.pos = (self.pos + 1) % len(self.button_positions)
        self.ball.pixmap_item.setPos(self.button_positions[self.pos])
        self.current_label = self.button_labels[self.pos]

        # temporarily suspend sampling to allow eye to switch to new location
        self.sample_timer.stop()
        QTimer.singleShot(500, self.start_sampling)

    def start_sampling(self):
        if self.sample_timer:
            self.sample_timer.start(5)

    def endBallAnimation(self):
        self.scene.removeItem(self.ball.pixmap_item)
        self.sample_timer.stop()
        self.sample_timer = None
        self.position_timer.stop()
        del self.position_timer
        self.ball.deleteLater()
        del self.ball

        self.initPostBallMessage()

    def centerTextbox(self):
        self.textbox.setMinimumWidth(self.textbox.document().size().width())
        self.textbox.setMinimumHeight(self.textbox.document().size().height())
        self.textbox.move((self.screen_width - self.textbox.width()) / 2, (self.screen_height - self.textbox.height()) / 2)


    def initPostBallMessage(self):
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.setFrameStyle(0)

        self.textbox.setHtml("""
            <p>The data will now be sent to our database.</p>
            <p>The data will now be sent to our database.</p>
        """)

        self.textbox.setLineWrapMode(0)

        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.show()

        self.finished_calibration = False

        QTimer.singleShot(3000, self.endPostBallMessage)

        if self.train_at_end:
            text = """
                <h2>Data gathering complete!</h2>
                <p>Calibrating ...</p>
            """
            self.textbox.setHtml(text)
            self.centerTextbox()

            thread = Thread(target=self.train_machine_learning)
            thread.start()

        else:
            text = """
                <h2>Data gathering complete!</h2>
                <p>The data will now be sent to our database.</p>
            """
            self.textbox.setHtml(text)
            self.centerTextbox()
            self.sendData()

    def endPostBallMessage(self):
        if self.finished_calibration:
            self.close()
            self.parent.set_active_widget(1)
        else:
            if self.train_at_end:
                training_pct = int(100 * self.detector.current_epoch / self.detector.training_epochs)
                accuracy = round(100 * self.detector.current_accuracy, 1)
                text = """
                    <h2>Data gathering complete!</h2>
                    <p>Calibrating ...  {pct}%</p>
                    <p>Expected Accuracy: {acc}%</p>
                """.format(pct=training_pct, acc=accuracy)

                self.textbox.setHtml(text)

            QTimer.singleShot(250, self.endPostBallMessage)

    def sendData(self):
        data = self.parseData(self.data, True)
        client = MongoClient('mongodb://JohnH:johnhoward@ds231228.mlab.com:31228/eyedata-devel')
        db = client['eyedata-devel']
        collection = db.Test

        user = getuser()

        data_to_send = [{'x': [float(n) for n in x], 'y': y, 'name': user} for x, y in data]
        collection.insert_many(data_to_send)

        self.finished_calibration = True

    def parseData(self, inputData, check_blinks=False):
        final_data = []

        last_id = -1

        for x, y in inputData:
            data_id = x[0]

            if data_id != last_id:
                if check_blinks and self.detector.detect_blink(x):
                    continue
                final_data.append((x, y))

            last_id = data_id

        return final_data

    def augment_data(self, data, labels):
        final_data = []
        final_labels = []

        for features, label in zip(data, labels):
            final_data.append(features)
            final_labels.append(label)

            # create changed vector here
            new_features = [n + gauss(0, 0.005) for n in features]
            final_data.append(new_features)
            final_labels.append(label)

        return final_data, final_labels

    def train_machine_learning(self):
        filtered_data = self.parseData(self.data)
        training_data = []
        training_labels = []

        for x, y in filtered_data:
            x_vector = self.detector.extract_used_features(x)
            training_data.append(x_vector)
            training_labels.append(y)

        try:
            left_eye_ratios = [features[0][1] for features in filtered_data if features[1] in (2, 3, 5, 6, 7, 8)]
            twenty_pct = len(left_eye_ratios) // 5
            left_eye_ratios = sorted(left_eye_ratios)[twenty_pct: -twenty_pct]
            right_eye_ratios = [features[0][2] for features in filtered_data if features[1] in (2, 3, 5, 6, 7, 8)]
            right_eye_ratios = sorted(right_eye_ratios)[twenty_pct: -twenty_pct]
            baseline_eye_ratio = (sum(left_eye_ratios) + sum(right_eye_ratios)) / (2 * len(left_eye_ratios))
            self.detector.set_new_blink_threshold(baseline_eye_ratio)
        except ZeroDivisionError:
            pass

        training_data, training_labels = self.augment_data(training_data, training_labels)

        self.detector.train_location_classifier(training_data, training_labels)
        self.finished_calibration = True

        accuracy = self.detector.current_accuracy

        if accuracy >= 0.6:
            self.sendData()

        self.finished_calibration = True

    def sample_features(self):
        features = self.detector.sample_features()
        label = self.current_label
        self.data.append((features, label))
