from PyQt5 import QtWidgets
from pythontools.gui.object import Object

class EditText(Object):

    def __init__(self, window):
        super(EditText, self).__init__(window)
        self.obj = QtWidgets.QPlainTextEdit(window.window)

    def setText(self, text):
        self.obj.insertPlainText(text)
        return self

    def getText(self):
        return self.obj.toPlainText()


class EditLine(Object):

    def __init__(self, window):
        super(EditLine, self).__init__(window)
        self.obj = QtWidgets.QLineEdit(window.window)

    def setToPasswordField(self):
        self.obj.setEchoMode(QtWidgets.QLineEdit.Password)
        return self

    def setReadOnly(self, bool):
        self.obj.setReadOnly(bool)
        return self

    def setPlaceholderText(self, text):
        self.obj.setPlaceholderText(text)
        return self

    def setText(self, text):
        self.obj.setText(text)
        return self

    def onChange(self, on_change):
        self.obj.textChanged.connect(on_change)
        return self

    def onEnter(self, on_enter):
        self.obj.returnPressed.connect(on_enter)
        return self

    def getText(self):
        return self.obj.text()