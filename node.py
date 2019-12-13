from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

class SSNode(object):

    def __init__(self):
        self.name = ''

        self.input_plugs = []
        self.output_plugs = []

class SSRenderNode(QWidget):

    def __init__(self):
        super(SSRenderNode, self).__init__()
        pass