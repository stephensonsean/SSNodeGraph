from graphics import *


class NodeGraphNodeScene(object):

    def __init__(self):

        self.width = 32000
        self.height = 32000

        self.nodes = []
        self.connectors = []

        self.init_ui()

    def init_ui(self):
        self.render_scene = NodeGraphGraphicsScene(self)
        self.render_scene.set_scene(self.width, self.height)

    def add_node(self, node):
        self.nodes.append(node)

    def add_connector(self, connector):
        self.connectors.append(connector)

    def remove_node(self, node):
        self.nodes.remove(node)

    def remove_connector(self, connector):
        self.connectors.remove(connector)