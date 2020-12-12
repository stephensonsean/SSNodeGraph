from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

import enum


class WireTypeEnum(enum.Enum):
    STRAIGHT = 0
    BEZIER = 1
    ANGLE = 2


class SSWire(object):
    def __init__(self, scene, in_port, out_port, wire_type=WireTypeEnum.STRAIGHT):
        self.in_port = in_port
        self.out_port = out_port
        self.type = type
        self.scene = scene

        self.render = SSWireRender(parent=self.scene)
        self.scene.render.addItem(self.render)

class SSWireRender(QGraphicsItem):
    def __init__(self, x1, y1, x2, y2, wire_type, parent=None):
        super(SSWireRender, self).__init__(parent=parent)

        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self._painter = QPainter()
        self._pen = QPen()
        self._color = QColor(255, 255, 0)
        self._line_type = Qt.SolidLine

    def paintEvent(self, e):
        pass


class SSWireRenderStraight(SSWireRender):
    def __init__(self, x1, y1, x2, y2, wire_type, parent=None):
        super(SSWireRenderStraight, self).__init__(x1=x1, y1=y1, x2=x2, y2=y2, wire_type=wire_type, parent=parent)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self._painter.begin(self)
        pen = QPen(self._color, 2, self._line_type)

        self._painter.setPen(pen)
        self._painter.drawLine(20, 40, 250, 40)

        self._painter.end()

    def updatePath(self):
        raise NotImplemented("Not Yet")

