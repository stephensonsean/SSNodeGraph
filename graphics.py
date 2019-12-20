from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import math


class NodeGraphGraphicsScene(QGraphicsScene):

    def __init__(self, scene, parent=None):
        super(NodeGraphGraphicsScene, self).__init__(parent)

        self.scene = scene

        self.grid_size = 17
        self.grid_square = 5

        self._bg_color = QColor("#333333")
        self._line_color = QColor("#444444")
        self._line_color_dark = QColor("#222222")

        self._pen_light = QPen(self._line_color)
        self._pen_light.setWidth(1)

        self._pen_dark = QPen(self._line_color_dark)
        self._pen_dark.setWidth(2)
        self.setBackgroundBrush(self._bg_color)
    
    def set_scene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2,
                          width, height)
    
    def drawBackground(self, painter, rect):
        super(NodeGraphGraphicsScene, self).drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light = []
        lines_dark = []

        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_square) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_square) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)
        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)


class NodeGraphGraphicsView(QGraphicsView):

    def __init__(self, gr_scene, parent=None):
        super(NodeGraphGraphicsView, self).__init__(parent)

        self.gr_scene = gr_scene

        self.init_ui()

        self.setScene(self.gr_scene)

        self.zoom = 10
        self.zoom_factor = .5
        self.zoom_clamp = False
        self.zoom_step = 1
        self.zoom_range = [0, 10]

    def init_ui(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.middle_mouse_button_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.middle_mouse_button_release(event)
        else:
            super().mouseReleaseEvent(event)

    def middle_mouse_button_press(self, event):
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                    Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        false_release_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                          Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(false_release_event)

    def middle_mouse_button_release(self, event):
        false_release_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                          Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(false_release_event)
        self.setDragMode(QGraphicsView.NoDrag)

    def left_mouse_button_press(self, event):
        return super().mousePressEvent(event)

    def left_mouse_button_release(self, event):
        return super().mouseReleaseEvent(event)

    def right_mouse_button_press(self, event):
        return super().mousePressEvent(event)

    def right_mouse_button_release(self, event):
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event:QWheelEvent):
        zoom_out = 1 / self.zoom_factor

        old_position = self.mapToScene(event.pos())

        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out
            self.zoom -= self.zoom_step

        clamped = False
        if self.zoom < self.zoom_range[0]: self.zoom, clamped = self.zoom_range[0], True
        if self.zoom > self.zoom_range[1]: self.zoom, clamped = self.zoom_range[1], True

        if not clamped or self.zoom_clamp is False:
            self.scale(zoom_factor, zoom_factor)

        new_position = self.mapToScene(event.pos())
        delta = new_position - old_position
        self.translate(delta.x(), delta.y())
        self.translate(100.00, 100.00)