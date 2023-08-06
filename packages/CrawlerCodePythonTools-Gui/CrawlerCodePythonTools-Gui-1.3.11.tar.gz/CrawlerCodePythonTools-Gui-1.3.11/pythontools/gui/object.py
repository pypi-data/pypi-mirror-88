from PyQt5 import QtGui

class Object:

    def __init__(self, window):
        self.window = window
        self.styles = []

    def setPosition(self, x, y):
        self.obj.move(x, y)
        return self

    def setSize(self, width, height):
        self.obj.setFixedSize(width, height)
        return self

    def setFont(self, name="Times", size=10, bold=False):
        self.obj.setFont(QtGui.QFont(name, size, QtGui.QFont.Normal if bold is False else QtGui.QFont.Bold))
        return self

    def setColor(self, color):
        self.styles.append("color:" + color)
        self.obj.setStyleSheet(type(self.obj).__name__ + "{" + ";".join(self.styles) + "}")
        return self

    def setBackgroundColor(self, color):
        self.styles.append("background-color:" + color)
        self.obj.setStyleSheet(type(self.obj).__name__ + "{" + ";".join(self.styles) + "}")
        return self

    def setBorderRadius(self, radius):
        self.styles.append("border-radius:" + radius)
        self.obj.setStyleSheet(type(self.obj).__name__ + "{" + ";".join(self.styles) + "}")
        return self

    def setEnabled(self, bool):
        self.obj.setEnabled(bool)

    def hasFocus(self):
        return self.obj.hasFocus()