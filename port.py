from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import enum


class PortPosition(enum.Enum):
    LEFT_TOP = 1
    LEFT_BTM = 2
    RIGHT_TOP = 3
    RIGHT_BTM = 4


class Port(object):
    def __init__(self, node, index=0, position=PortPosition.LEFT_TOP):
        self.node = node
        self.index = index
        self.position = position

        self.render = PortRender(self.node.render)
        self.render.setPos(*self.node.port_pos(index=self.index, position=self.position))


class PortRender(QGraphicsItem):
    def __init__(self, parent=None):
        super(PortRender, self).__init__(parent=parent)

        self.radius = 8
        self.outline_width = 1.0
        self._background = QColor("#FFFF7700")
        self._outline = QColor("#FF000000")

        self._pen = QPen(self._outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)

    def boundingRect(self):
        return QRectF(-self.radius - self.outline_width,
                      -self.radius - self.outline_width,
                      2 * (self.radius + self.outline_width),
                      2 * (self.radius + self.outline_width))