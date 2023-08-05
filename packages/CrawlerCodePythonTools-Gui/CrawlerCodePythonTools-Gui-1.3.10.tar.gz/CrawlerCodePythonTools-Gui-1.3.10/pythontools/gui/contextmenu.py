from PyQt5 import QtWidgets

class ContextMenu:

    def __init__(self):
        self.menu = QtWidgets.QMenu()

    def addActions(self, actions):
        for action in actions:
            self.menu.addAction(action)
        return self

    def createAction(self, name, function, shortcut=None):
        action = QtWidgets.QAction(name, self.menu, triggered=function)
        if shortcut is not None:
            action.setShortcut(shortcut)
        return action