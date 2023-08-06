from PyQt5 import QtWidgets, QtGui
import base64

class ContextMenu:

    def __init__(self, menu=None):
        self.menu = menu if menu is not None else QtWidgets.QMenu()

    def addActions(self, actions):
        for action in actions:
            self.menu.addAction(action)
        return self

    def createAction(self, name, function, shortcut=None, icon=None):
        action = QtWidgets.QAction(name, self.menu, triggered=function)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(icon)
        return action

    def addAction(self, name, function, shortcut=None, icon=None):
        action = QtWidgets.QAction(name, self.menu, triggered=function)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(icon)
        self.menu.addAction(action)
        return self

    def createIcon(self, b64):
        if b64.startswith('data:image/png;base64,'):
            b64 = b64.replace('data:image/png;base64,', "")
        icon = QtGui.QIcon()
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(b64))
        icon.addPixmap(pm)
        return icon

    def addMenu(self, name, icon=None):
        if icon is not None:
            return ContextMenu(self.menu.addMenu(icon, name))
        else:
            return ContextMenu(self.menu.addMenu(name))