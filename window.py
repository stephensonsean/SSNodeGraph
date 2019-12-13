from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from graphics import *
from scene import *


class NodeGraphWindow(QWidget):

    def __init__(self, parent=None):

        super(NodeGraphWindow, self).__init__(parent)

        self.init_ui()

    def init_ui(self):

        self.setGeometry(200, 200, 1000, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)

        self.setLayout(self.layout)

        self.scene = NodeGraphNodeScene()

        self.view = NodeGraphGraphicsView(self.scene.render_scene)

        self.layout.addWidget(self.view)

        self.setWindowTitle("S.S. Node Graph")
        self.show()

        self.add_content()

    def add_content(self):
            self.magenta_brush = QBrush(Qt.darkRed)

            self.outline = QPen(Qt.red)
            self.outline.setWidth(2)

            rect = self.scene.render_scene.addRect(-100, -100, 80, 100, self.outline, self.magenta_brush)
            rect.setFlag(QGraphicsItem.ItemIsMovable)

    def keyPressEvent(self, event:QKeyEvent):
        print(event.key())
        if event.key() == Qt.Key_D:
            rect = self.scene.render_scene.addRect(-100, -100, 80, 100, self.outline, self.magenta_brush)
            rect.setFlag(QGraphicsItem.ItemIsMovable)
        elif event.key() == Qt.Key_R:
            self.scene.render_scene.setSceneRect(-self.scene.render_scene.scene_width // 2, -self.scene.render_scene.scene_height // 2,
                                              self.scene.render_scene.scene_width, self.scene.render_scene.scene_height)