from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from graphics import *
from scene import *
from node import *


class NodeGraphWindow(QWidget):

    def __init__(self, parent=None):

        super(NodeGraphWindow, self).__init__(parent)

        self.style_sheet = 'style_sheet.css'
        self.load_style_sheet(self.style_sheet)

        self.init_ui()

    def init_ui(self):

        self.setGeometry(200, 200, 1000, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)

        self.setLayout(self.layout)

        self.scene = NodeGraphNodeScene()

        node = SSNode(self.scene, "MultiplyDivide", inputs=[1, 2], outputs=[1])

        self.view = NodeGraphGraphicsView(self.scene.render_scene, self)

        self.layout.addWidget(self.view)

        self.setWindowTitle("S.S. Node Graph")
        self.show()

    def add_content(self):
        SSNode(self.scene, "ArmIk_L_md")

    def load_style_sheet(self, style_sheet_file=''):
        file = QFile(style_sheet_file)
        file.open(QFile.ReadOnly | QFile.Text)
        style_sheet = file.readAll()
        QApplication.instance().setStyleSheet(str(style_sheet, encoding='utf-8'))

    def keyPressEvent(self, event:QKeyEvent):
        print(event.key())
        if event.key() == Qt.Key_D:
            self.add_content()
            #rect = self.scene.render_scene.addRect(-100, -100, 80, 100, self.outline, self.magenta_brush)
            # rect.setFlag(QGraphicsItem.ItemIsMovable)
        elif event.key() == Qt.Key_R:
            self.scene.render_scene.setSceneRect(-self.scene.width // 2, -self.scene.height // 2,
                                                 self.scene.width, self.scene.height)