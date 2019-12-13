import sys
from PySide2.QtWidgets import *
from window import*


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = NodeGraphWindow()

    sys.exit(app.exec_())