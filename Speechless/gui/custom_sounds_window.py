from PyQt5 import uic
from PyQt5 import QtWidgets
from pathlib import Path
from Speechless.utils import settings_util


rel_dir = str(Path.cwd())
sounds_dir = rel_dir + '\\sounds'
FormClass, BaseClass = uic.loadUiType(rel_dir + '\\layouts\\custom_sounds_window.ui')


class CustomSoundsWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(CustomSoundsWindow, self).__init__()
        self.parent_app = app
        self.setupUi(self)

        self.mute_browse_dialog = None
        self.unmute_browse_dialog = None
        self.mute_sound_filename = None
        self.unmute_sound_filename = None

        self.mute_browse_button = self.findChild(QtWidgets.QPushButton, 'muteBrowseButton')
        self.mute_browse_button.clicked.connect(self.mute_browse_button_cb)

        self.unmute_browse_button = self.findChild(QtWidgets.QPushButton, 'unmuteBrowseButton')
        self.unmute_browse_button.clicked.connect(self.unmute_browse_button_cb)

    def mute_browse_button_cb(self):
        self.mute_browse_dialog = QtWidgets.QFileDialog()
        path = sounds_dir
        self.mute_sound_filename = QtWidgets.QFileDialog.getOpenFileName(self.mute_browse_dialog, "", path)
        self.parent_app.settings.setting["sound_files"][0]["mute_sound"] = self.mute_sound_filename[0]
        settings_util.write_settings(self.current_settings)

    def unmute_browse_button_cb(self):
        self.unmute_browse_dialog = QtWidgets.QFileDialog()
        path = sounds_dir
        self.unmute_sound_filename = QtWidgets.QFileDialog.getOpenFileName(self.mute_browse_dialog, "", path)
        self.parent_app.settings.setting["sound_files"][1]["unmute_sound"] = self.unmute_sound_filename[0]
        settings_util.write_settings(self.parent_app.settings)
