from PyQt5 import uic, QtGui
from Speechless.utils import files_util


about_window_layout_file = files_util.get_layouts_dir().joinpath('about_window.ui')
files_util.dep_check(about_window_layout_file)
FormClass, BaseClass = uic.loadUiType(about_window_layout_file)


class AboutWindow(BaseClass, FormClass):
    """Creates a AboutWindow object for the GUI based on the about_window_layout_file."""

    def __init__(self):
        super(AboutWindow, self).__init__()

        # Setup
        self.setupUi(self)
        icon_filepath = files_util.get_icons_dir().joinpath('mic.png')
        files_util.dep_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))
