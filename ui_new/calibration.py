from PyQt5.QtWidgets import (QApplication, QGraphicsView,
        QGraphicsPixmapItem, QGraphicsScene, QDesktopWidget, QTextEdit)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import (QObject, QPointF, QTimer,
        QPropertyAnimation, pyqtProperty, Qt)
import sys
from multiprocessing import Process, Queue
from ui_layout import build_layout_dictionary


class Ball(QObject):
    def __init__(self):
        super().__init__()

        self.pixmap_item = QGraphicsPixmapItem(QPixmap("red_ball.png"))

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class Calibration(QGraphicsView):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.initView()
        self.data = []

    def initView(self):
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

        timer = QTimer(self)
        timer.timeout.connect(self.endPreBallMessage)
        timer.start(1000)
        self.timer = timer

    def endPreBallMessage(self):
        self.textbox.deleteLater()
        self.textbox.hide()
        del self.textbox

        self.timer.stop()
        self.initBallAnimation()

    def initBallAnimation(self):
        self.ball = Ball()
        self.ball_width = self.ball.pixmap_item.boundingRect().size().width()
        self.ball_height = self.ball.pixmap_item.boundingRect().size().height()

        sg = QDesktopWidget().screenGeometry()
        layout = build_layout_dictionary(sg.width(), sg.height())
        elements = layout['elements']

        self.pos = 0
        self.button_positions = [QPointF(elem['top_left_x'] + elem['width'] / 2 - self.ball_width / 2,
                                         elem['top_left_y'] + elem['height'] / 2 - self.ball_height / 2)
                                 for _, elem in elements.items()]

        self.ball.pixmap_item.setPos(self.button_positions[0])

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.screen_width, self.screen_height)
        self.scene.addItem(self.ball.pixmap_item)
        self.setScene(self.scene)

        self.position_timer = QTimer()
        self.position_timer.timeout.connect(self.move_ball)
        self.position_timer.start(1250)

        # self.sample_timer = QTimer(self)
        # self.sample_timer.timeout.connect(self.sample_features)
        # self.sample_timer.start(5)

        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.endBallAnimation)
        self.end_timer.start(1250 * len(self.button_positions) * 2)


    def move_ball(self):
        next_position = (self.pos + 1) % len(self.button_positions)
        self.ball.pixmap_item.setPos(self.button_positions[next_position])
        self.pos += 1

    def endBallAnimation(self):
        self.scene.removeItem(self.ball.pixmap_item)
        # self.sample_timer.stop()
        # self.sample_timer = None
        self.end_timer.stop()
        del self.end_timer
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

        text = """
            <h2>Data gathering complete!</h2>
            <p>The data will now be sent to our database</p>
        """

        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setHtml(text)
        self.textbox.show()

        self.dataSent = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.endPostBallMessage)
        self.timer.start(1000)

        self.sendData()

    def endPostBallMessage(self):
        if self.dataSent:
            self.close()
            self.parent.stacked_widget.setCurrentIndex(1)

    def sendData(self):
        self.dataSent = True

        # TODO: Implement data send to database

    def sample_features(self, detector, queue, pos):
        x, y = int(pos.x()) + self.ball_width / 2, int(pos.y()) + self.ball_height / 2

        x_max, y_max = self.screen_width, self.screen_height
        features = detector.sample_features_mock()
        queue.put((features, [x, y, x_max, y_max]))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calibration()
    sys.exit(app.exec_())
