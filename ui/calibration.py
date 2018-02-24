from threading import Thread
from pymongo import MongoClient
from PyQt5.QtWidgets import (QGraphicsView,
        QGraphicsPixmapItem, QGraphicsScene, QDesktopWidget, QTextEdit)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import (QObject, QPointF, QTimer, pyqtProperty, Qt)
from ui.ui_layout import build_layout_dictionary


EACH_BUTTON_TIME = 1500


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
        self.initPreBallMessage()

    def initView(self):
        self.showFullScreen()

        self.sg = QDesktopWidget().screenGeometry()
        self.screen_width = self.sg.width()
        self.screen_height = self.sg.height()

        self.setWindowTitle("Calibration")
        self.setRenderHint(QPainter.Antialiasing)


    def initPreBallMessage(self):
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.move(self.screen_width / 2 - self.textbox.width(), self.screen_height / 2 - self.textbox.height())
        text = """
            <h2>Calibration</h2>
            <p>Please follow the red ball as it jumps around</p>
        """

        self.textbox.setHtml(text)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setFrameStyle(0)
        self.textbox.show()

        QTimer.singleShot(3000, self.endPreBallMessage)

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
        elements = layout['elements']

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

        total_timeout = EACH_BUTTON_TIME * len(self.button_positions) * 2
        QTimer.singleShot(total_timeout, self.endBallAnimation)

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

    def initPostBallMessage(self):
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setFrameStyle(0)

        self.textbox.move(self.screen_width / 2 - self.textbox.width(), self.screen_height / 2 - self.textbox.height())
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.show()

        self.finished_calibration = False

        QTimer.singleShot(3000, self.endPostBallMessage)

        if self.train_at_end:
            text = """
                <h2>Data gathering complete!</h2>
                <p>Calibrating...</p>
            """
            self.textbox.setHtml(text)

            thread = Thread(target=self.train_machine_learning)
            thread.start()

        else:
            text = """
                <h2>Data gathering complete!</h2>
                <p>The data will now be sent to our database.</p>
            """
            self.textbox.setHtml(text)
            self.sendData()

    def endPostBallMessage(self):
        if self.finished_calibration:
            self.close()
            self.parent.set_active_widget(1)
        else:
            QTimer.singleShot(1000, self.endPostBallMessage)

    def sendData(self):
        data = self.parseData(self.data)
        client = MongoClient('mongodb://JohnH:johnhoward@ds231228.mlab.com:31228/eyedata-devel')
        db = client['eyedata-devel']
        collection = db.Test

        data_to_send = [{'x': x, 'y': y} for x, y in data]
        insertTest = collection.insert_many(data_to_send)
        # insertTest.inserted_ids

        self.finished_calibration = True

    def parseData(self, inputData):
        final_data = []

        last_id = -1

        for x, y in inputData:
            data_id = x[0]
            if data_id == last_id:
                final_data.append((x, y))

            last_id = data_id

        return final_data

    def train_machine_learning(self):
        filtered_data = self.parseData(self.data)
        training_data = []
        training_labels = []

        for x, y in filtered_data:
            x_vector = self.detector.extract_used_features(x)
            training_data.append(x_vector)
            training_labels.append(y)

        self.detector.train_location_classifier(training_data, training_labels)
        self.finished_calibration = True

        self.detector.test_accuracy(training_data, training_labels)

        self.finished_calibration = True

    def sample_features(self):
        features = self.detector.sample_features()
        label = self.current_label
        self.data.append((features, label))
