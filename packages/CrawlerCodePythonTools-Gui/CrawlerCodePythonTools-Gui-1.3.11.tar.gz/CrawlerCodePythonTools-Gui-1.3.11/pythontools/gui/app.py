from PyQt5 import QtWidgets, QtGui, QtCore
import sys, base64


class App(object):

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet("QMainWindow { border: 1px solid #242424; }")

    def setIcon(self, b64):
        icon = QtGui.QIcon()
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(b64))
        icon.addPixmap(pm)
        self.app.setWindowIcon(icon)
        return self

    def setDarkStyle(self):
        css = """
            QMainWindow, QDialog { 
                background-color: #363636;
            }

            QLineEdit, QPlainTextEdit, QListWidget, QMenu { 
                background-color: #363636; 
                color: #d4d4d4;
            }

            QLabel {
                color: #d4d4d4;
            }

            QMenuBar, QPushButton {
                background-color: #141414;
                color: #d4d4d4;
            }

            QMenuBar::item::selected  {
                background-color: #3b3b3b;
            }

            QPushButton::hover {
                background-color: #242424;
            }

            QMenu::item {
                background-color: #454545;
            }

            QMenu::item:selected {
                background-color: #737373;
            }

            """
        self.app.setStyleSheet(css)
        return self

    def onClipboardChanged(self, function):
        self.app.clipboard().dataChanged.connect(lambda: function(self.getClipboard()))

    def setClipboard(self, text=None, files=None):
        data = QtCore.QMimeData()
        if text is not None:
            data.setText(text)
        if files is not None:
            urls = []
            for f in files:
                urls.append(QtCore.QUrl.fromLocalFile(f))
            data.setUrls(urls)
        self.app.clipboard().setMimeData(data)

    def getClipboard(self):
        return self.app.clipboard().text()

    def start(self):
        sys.exit(self.app.exec_())

    def exit(self):
        self.app.exit()