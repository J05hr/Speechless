from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon_filename, app, main_window):
        icon = QtGui.QIcon(icon_filename)
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent=None)
        self.parent_app = app
        self.main_window = main_window
        self.setToolTip('Speechless v1.0')

        # menu options
        self.menu = QtWidgets.QMenu(parent=None)
        self.action_open = QtWidgets.QAction("Open")
        self.action_open.triggered.connect(self.open_action_cb)
        self.action_quit = QtWidgets.QAction("Quit")
        self.action_quit.triggered.connect(self.quit_action_cb)
        self.menu.addAction(self.action_open)
        self.menu.addAction(self.action_quit)
        self.setContextMenu(self.menu)

    # open main window
    def open_action_cb(self):
        if self.main_window.windowState() == QtCore.Qt.WindowMinimized:
            # Window is minimised. Restore it.
            self.main_window.setWindowState(QtCore.Qt.WindowNoState)
        if self.main_window.isHidden():
            self.main_window.show()

    # quit application
    def quit_action_cb(self):
        self.parent_app.quit()
