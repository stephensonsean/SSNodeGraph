from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from port import Port, PortPosition


class SSNode(object):

    def __init__(self, scene, name, inputs=[], outputs=[]):
        """

        Args:
            scene (NodeGraphNodeScene):
            name (str):
        """
        self.name = name
        self.scene = scene

        self.content = []
        self.populate_content()
        self.render = SSNodeRender(self, self.name)

        self.scene.add_node(self)
        self.scene.render_scene.addItem(self.render)

        self.input_plugs = []
        self.output_plugs = []

        self.port_spacing = 24

        count = 0
        for item in inputs:
            port = Port(node=self, index=count)
            self.input_plugs.append(port)
            count += 1

        count = 0
        for item in outputs:
            port = Port(node=self, index=count, position=PortPosition.RIGHT_BTM)
            self.output_plugs.append(port)
            count += 1

    def populate_content(self):
        self.content.append( SSNodeContentRender( attribute_name='input1X', attribute_type='1.0'))
        self.content.append( SSNodeContentRender( attribute_name='active', attribute_type=True))

    def port_pos(self, index, position):
        x = 0 if position in [PortPosition.LEFT_TOP, PortPosition.LEFT_BTM] else self.render.width
        if position in [PortPosition.LEFT_BTM, PortPosition.RIGHT_BTM]:
            y = self.render.height - self.render.edge_size - self.render._padding - index * self.port_spacing
        else:
            y = self.render.title_height + self.render._padding + self.render.edge_size + index * self.port_spacing

        return x, y


class SSNodeRender(QGraphicsItem):
    def __init__(self, node, title='Node Graphics Item', parent=None):
        super().__init__(parent=parent)

        self._title_color = Qt.white
        self._title_font = QFont("CaviarDreamsRegular", 12)

        self.width = 180
        self.height = 100
        self.edge_size = 10.0
        self.title_height = 29.0
        self._padding = 4.0

        self.content = node.content
        self.content_height = 27
        self.content_width = 162
        self.content_padding = 2.5

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor(70,70,70))
        self._brush_background = QBrush(QColor(22,22,22))

        self.init_title()
        self.title = title

        self.init_content()

        self.init_ui()

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height).normalized()

    def init_ui(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def init_title(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, -4)
        self.title_item.setTextWidth(self.width - 2 * self._padding)

    def init_content(self):
        height = self.content_padding+ self.title_height
        for item in self.content:

            self.render_content = QGraphicsProxyWidget(self)
            item.setGeometry(15,
                             height,
                             self.content_width,
                             self.content_height)
            self.render_content.setWidget(item)

            height += self.content_height + self.content_padding

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRect(0, 0, self.width, self.title_height, )
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size,
                           self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRect(0, self.title_height, self.width, self.height - self.title_height, )
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRect(0, 0, self.width, self.height)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())


class SSNodeContentRender(QWidget):

    def __init__(self, parent=None, attribute_name='Attribute', attribute_type=None):
        super(SSNodeContentRender, self).__init__(parent=parent)

        self.attribute_type = attribute_type
        self.attribute_name = attribute_name

        self.layout = QHBoxLayout()
        self.widget = QWidget
        self.label = QLabel(self.attribute_name)
        self.label.setFont(QFont('Ariel', 100))

        self.__set_widget_based_on_attr_type()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.widget)

        self.layout.setContentsMargins(4, 1, 1, 1)
        self.setLayout(self.layout)

    def __set_widget_based_on_attr_type(self):
        if isinstance(self.attribute_type, str):
            self.widget = QLineEdit('')
            self.widget
        if isinstance(self.attribute_type, bool):
            self.widget = QCheckBox()
            self.widget.setChecked(self.attribute_type)