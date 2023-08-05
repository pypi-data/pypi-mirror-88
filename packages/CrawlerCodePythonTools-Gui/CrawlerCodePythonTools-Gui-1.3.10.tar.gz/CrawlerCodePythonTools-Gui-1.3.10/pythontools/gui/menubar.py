from PyQt5 import QtWidgets

class MenuBar:

    def __init__(self, window):
        self.window = window
        self.obj = window.window.menuBar()
        self.menues = {}
        self.on_clicks = {}

    def addMenu(self, name):
        menu = self.obj.addMenu(name)
        self.menues[name] = menu

        def triggered(e):
            _name = name + "." + e.text()
            if _name in self.on_clicks:
                self.on_clicks[_name]()

        menu.triggered[QtWidgets.QAction].connect(triggered)
        return self

    def addAction(self, menu, name, shortcut=None, on_click=None):
        action = QtWidgets.QAction(name, self.window.window)
        if shortcut is not None:
            action.setShortcut(shortcut)
        self.menues[menu].addAction(action)
        if on_click is not None:
            self.on_clicks[menu + "." + name] = on_click
        return self