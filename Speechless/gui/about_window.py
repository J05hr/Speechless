from PyQt5 import uic
from pathlib import Path


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\about_window.ui')


class AboutWindow(BaseClass, FormClass):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)
