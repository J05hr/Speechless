from PyQt5 import uic, QtGui
from pathlib import Path


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\about_window.ui')


class AboutWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(AboutWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(app.icons_dir + '\\mic.png'))
