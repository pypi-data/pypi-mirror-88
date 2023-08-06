from PyQt5 import QtWidgets, QtGui
import base64

class SystemTray:

    def __init__(self, app):
        self.tray = QtWidgets.QSystemTrayIcon(app.app)
        self.tray.setIcon(app.app.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

    def setIcon(self, b64):
        icon = QtGui.QIcon()
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(b64))
        icon.addPixmap(pm)
        self.tray.setIcon(icon)
        return self

    def setContextMenu(self, menu):
        self.tray.setContextMenu(menu.menu)
        return self

    def show(self):
        self.tray.show()
        return self

    def showMessage(self, title, message, duration=3000):
        self.tray.showMessage(title, message, QtWidgets.QSystemTrayIcon.Information, duration)
        return self