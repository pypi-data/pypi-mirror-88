from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

class Window(object):

    def __init__(self, title, width, height):
        self.window = QtWidgets.QDialog(None)
        self.window.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.window.setWindowTitle(title)
        self.window.setFixedSize(width, height)
        self.hidden = True

    def setPosition(self, x, y):
        self.window.move(x, y)
        return self

    def onClose(self, on_close):
        self.window.closeEvent = on_close
        return self

    def setTitle(self, title):
        self.window.setWindowTitle(title)
        return self

    def setAcceptDrops(self, bool):
        self.window.setAcceptDrops(bool)
        return self

    def setEnabled(self, bool):
        self.window.setEnabled(bool)

    def onKeyPress(self, function):
        def keyPressEvent(event):
            function(event.key())

        self.window.keyPressEvent = keyPressEvent
        return self

    def openFileDialog(self, name, file="", validFiles="All Files (*)"):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.window, name, file, validFiles, options=options)
        if fileName:
            return fileName
        return None

    def saveFileDialog(self, name, file="", validFiles="All Files (*)"):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.window, name, file, validFiles, options=options)
        if fileName:
            return fileName
        return None

    def setFlags(self, flags):
        self.window.setWindowFlags(flags)
        return self

    def setTransparentBackground(self):
        self.window.setAttribute(Qt.WA_TranslucentBackground, True)
        return self

    def show(self):
        self.window.show()
        self.hidden = False
        return self

    def hide(self):
        self.window.hide()
        self.hidden = True
        return self

    def close(self):
        self.window.close()
        return self

    def destroy(self):
        self.window.destroy()
        return self


class MainWindow(Window):

    def __init__(self, title, width, height):
        self.window = QtWidgets.QMainWindow(None)
        self.window.setWindowTitle(title)
        self.window.setFixedSize(width, height)

    def showMessage(self, text, duration=3000, color=None):
        self.window.statusBar().showMessage(text, duration)
        if color is not None:
            self.window.statusBar().setStyleSheet("QStatusBar { color: " + color + " }")
        return self