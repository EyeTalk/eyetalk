from PyQt5.QtWidgets import (QApplication, QGraphicsView,
        QGraphicsPixmapItem, QGraphicsScene, QDesktopWidget, QTextEdit)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import (QObject, QPointF, QTimer,
        QPropertyAnimation, pyqtProperty, Qt)
import sys
from GazeDetector import GazeDetector
from pymongo import MongoClient


class Ball(QObject):
    def __init__(self):
        super().__init__()

        self.pixmap_item = QGraphicsPixmapItem(QPixmap("red_ball.png"))

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class Example(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.initView()
        self.data = []

    def initView(self):
        self.gaze = GazeDetector()

        if not self.gaze.active:
            app.quit()

        self.showFullScreen()

        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        self.screen_width = ag.width()
        self.screen_height = ag.height()

        self.setWindowTitle("Calibration")
        self.setRenderHint(QPainter.Antialiasing)

        self.initPreBallMessage()


    def initPreBallMessage(self):
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.move(self.screen_width / 2 - self.textbox.width(), self.screen_height / 2 - self.textbox.height())
        text = """
            <h2>Calibration GUI</h2>
            <p>Please stare at the red ball while it moves</p>
            <p>Ball will begin in the top left corner</p>
        """

        self.textbox.setHtml(text)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setFrameStyle(0)
        self.textbox.show()

        sample_timer = QTimer(self)
        sample_timer.timeout.connect(self.endPreBallMessage)
        sample_timer.start(5000)
        self.sample_timer = sample_timer

    def endPreBallMessage(self):
        self.textbox.deleteLater()
        self.textbox.hide()
        del self.textbox

        self.sample_timer.stop()
        self.initBallAnimation()

    def initBallAnimation(self):
        self.ball = Ball()
        self.ball_width = self.ball.pixmap_item.boundingRect().size().width()
        self.ball_height = self.ball.pixmap_item.boundingRect().size().height()

        anim = QPropertyAnimation(self.ball, b'pos')
        anim.setDuration(10000)

        w = self.screen_width / 8
        h = self.screen_height / 8

        anim.setStartValue(QPointF(w, h))

        anim.setKeyValueAt(0.25, QPointF(7 * w - self.ball_width, h))
        anim.setKeyValueAt(0.5, QPointF(7 * w - self.ball_width, 7 * h - self.ball_height))
        anim.setKeyValueAt(0.75, QPointF(w, 7 * h - self.ball_height))

        anim.setEndValue(QPointF(w, h))

        self.anim = anim

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.screen_width, self.screen_height)
        self.scene.addItem(self.ball.pixmap_item)
        self.setScene(self.scene)

        self.sample_timer = QTimer(self)
        self.sample_timer.timeout.connect(self.sample_features)
        self.sample_timer.start(5)

        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.endBallAnimation)
        self.end_timer.start(10000)

        self.anim.start()

    def endBallAnimation(self):
        self.scene.removeItem(self.ball.pixmap_item)
        self.sample_timer.stop()
        self.sample_timer = None
        self.end_timer.stop()
        del self.end_timer
        self.ball.deleteLater()
        del self.ball

        self.initPostBallMessage()

    def initPostBallMessage(self):
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setFrameStyle(0)

        self.textbox.move(self.screen_width / 2 - self.textbox.width(), self.screen_height / 2 - self.textbox.height())

        text = """
            <h2>Data gathering complete!</h2>
            <p>The data will now be sent to our database</p>
        """

        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setHtml(text)
        self.textbox.show()

        self.dataSent = False

        self.sample_timer = QTimer(self)
        self.sample_timer.timeout.connect(self.endPostBallMessage)
        self.sample_timer.start(1000)

        self.sendData()

    def endPostBallMessage(self):
        if self.dataSent:
            app.quit()

    def format_data_for_machine_learning(self, data):
        final_data = []
        final_labels = []

        last_id = -1

        for x, y in data:
            data_id = x[0]
            if data_id == last_id:
                label = self.test_mapping(y)
                final_data.append(x[1:])
                final_labels.append(label)

            last_id = data_id

        return final_data, final_labels


    def sendData(self):
        # self.dataSent = True

        self.showMinimized()

        data, labels = self.format_data_for_machine_learning(self.data)

        self.gaze.train_location_classifier(data, labels, 20000)

        test_data = data[200]
        test_label = labels[200]

        new_label = self.gaze.calculate_location_probabilities_from_features(test_data)

        print(test_label, new_label)

        # self.dataSent = True

        client = MongoClient()
        client = MongoClient('mongodb://JohnH:johnhoward@ds231228.mlab.com:31228/eyedata-devel')
        db = client['eyedata-devel']
        collection = db.Test

        data_to_send = [{'x': x, 'y': y} for x, y in self.data]
        insertTest = db.Test.insert_many(data_to_send)
        insertTest.inserted_ids

    def test_mapping(self, label_data):
        x, y, width, height = label_data
        x_pct = x * 1.0 / width
        y_pct = y * 1.0 / height

        if x_pct < 0.5:
            if y_pct < 0.5:
                return 0
            else:
                return 2
        else:
            if y_pct < 0.5:
                return 1
            else:
                return 3

    def sample_features(self):
        current_pos = self.ball.pixmap_item.scenePos()
        
        x, y = int(current_pos.x()) + self.ball_width / 2, int(current_pos.y()) + self.ball_height / 2
        x_max, y_max = self.screen_width, self.screen_height

        features = self.gaze.sample_features()
        self.data.append((features, [x, y, x_max, y_max]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

