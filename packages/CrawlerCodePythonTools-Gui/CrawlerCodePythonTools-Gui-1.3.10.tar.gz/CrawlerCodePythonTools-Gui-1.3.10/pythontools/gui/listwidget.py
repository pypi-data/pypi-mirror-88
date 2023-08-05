from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from pythontools.gui.object import Object

class ListWidget(Object):

    def __init__(self, window):
        super(ListWidget, self).__init__(window)
        self.obj = QtWidgets.QListWidget(window.window)
        self.obj.setContextMenuPolicy(Qt.CustomContextMenu)

    def setContextMenu(self, actions, openOnylIfItemSelected=True):
        def rightMenuShow():
            if openOnylIfItemSelected is False or self.getSelectedItem() is not None:
                menu = QtWidgets.QMenu(self.obj)
                for action in actions:
                    menu.addAction(action)
                menu.exec_(QtGui.QCursor.pos())

        self.obj.customContextMenuRequested[QtCore.QPoint].connect(rightMenuShow)
        return self

    def createContextMenuAction(self, name, function):
        return QtWidgets.QAction(name, self.obj, triggered=function)

    def addItem(self, text, icon=None, toolTip=None):
        item = QtWidgets.QListWidgetItem(text)
        item.text()
        if icon is not None:
            item.setIcon(icon)
        if toolTip is not None:
            item.setToolTip(toolTip)
        item.toolTip()
        self.obj.addItem(item)
        return self

    def removeItem(self, text, toolTip=None):
        for i in range(self.obj.count()):
            item = self.obj.item(i)
            if item.text() == text and (toolTip is None or item.toolTip() == toolTip):
                self.obj.takeItem(i)

    def getSelectedItem(self):
        try:
            return self.obj.selectedItems()[0].text()
        except:
            return None

    def setAcceptDrops(self, bool):
        self.obj.setAcceptDrops(bool)
        return self

    def onFileDragEvent(self, function):
        def dragMoveEvent(event):
            if event.mimeData().hasUrls:
                event.setDropAction(Qt.CopyAction)
                event.accept()
            else:
                event.ignore()

        self.obj.dragMoveEvent = dragMoveEvent

        def dragEnterEvent(event):
            if event.mimeData().hasUrls:
                event.accept()
            else:
                event.ignore()

        self.obj.dragEnterEvent = dragEnterEvent

        def dropEvent(event):
            if event.mimeData().hasUrls:
                event.setDropAction(Qt.CopyAction)
                event.accept()
                files = []
                for url in event.mimeData().urls():
                    files.append(str(url.toLocalFile()))
                function(files)
            else:
                event.ignore()

        self.obj.dropEvent = dropEvent
        return self

    def onDoubleClick(self, on_double_click):
        self.obj.itemDoubleClicked.connect(on_double_click)
        return self