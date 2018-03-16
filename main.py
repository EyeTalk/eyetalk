import sys, os
from PyQt5.QtWidgets import QApplication

from ui.eyetalk_ui import MainUIWindow


if __name__ == '__main__':
    os.system("./build_backend.sh")
    app = QApplication(sys.argv)
    w = MainUIWindow()
    w.show()
    sys.exit(app.exec_())
