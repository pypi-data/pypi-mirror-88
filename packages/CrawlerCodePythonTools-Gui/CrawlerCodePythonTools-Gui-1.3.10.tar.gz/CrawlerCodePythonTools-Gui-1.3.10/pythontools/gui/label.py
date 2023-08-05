from PyQt5 import QtWidgets
from pythontools.gui.object import Object

class Label(Object):

    def __init__(self, window):
        super(Label, self).__init__(window)
        self.obj = QtWidgets.QLabel(window.window)

    def setText(self, text):
        self.obj.setText(text)
        return self

    def getText(self):
        return self.obj.text()