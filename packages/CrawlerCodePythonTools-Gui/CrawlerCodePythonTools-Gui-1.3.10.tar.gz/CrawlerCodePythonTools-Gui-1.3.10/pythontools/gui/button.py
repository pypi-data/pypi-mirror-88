from PyQt5 import QtWidgets
from pythontools.gui.object import Object

class Button(Object):

    def __init__(self, text, window):
        super(Button, self).__init__(window)
        self.obj = QtWidgets.QPushButton(text, window.window)

    def onClick(self, on_click):
        self.obj.clicked.connect(on_click)
        return self