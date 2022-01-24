from PyQt5 import uic, QtGui, QtCore, QtWidgets
from Speechless.utils import files_util


input_device_warning_layout_file = files_util.get_layouts_dir().joinpath('input_device_warning.ui')
files_util.dep_check(input_device_warning_layout_file)
FormClass, BaseClass = uic.loadUiType(input_device_warning_layout_file)


class InputDeviceWarningWindow(BaseClass, FormClass):
    """Creates a InputDeviceWarningWindow object for the GUI based on the input_device_warning_layout_file."""

    def __init__(self, gui_app):
        super(InputDeviceWarningWindow, self).__init__()

        # Setup
        self.setupUi(self)
        self.gui_app = gui_app
        icon_filepath = files_util.get_icons_dir().joinpath('mic.png')
        files_util.dep_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))

        # GUI components
        self.ok_button = self.findChild(QtWidgets.QPushButton, 'okButton')
        self.ok_button.clicked.connect(self.finished_cb)

    def finished_cb(self):
        """Callback for the ok action."""
        self.gui_app.quit()

    def closeEvent(self, _):
        self.gui_app.quit()

