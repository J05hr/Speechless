from pathlib import Path
from PyQt5 import uic, QtGui, QtWidgets
from Speechless.utils import settings_util


rel_dir = str(Path.cwd())
sounds_dir = rel_dir + '\\sounds'
FormClass, BaseClass = uic.loadUiType(rel_dir + '\\layouts\\custom_sounds_window.ui')


class CustomSoundsWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(CustomSoundsWindow, self).__init__()
        self.parent_app = app
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(app.icons_dir + '\\mic.png'))

        self.mute_browse_dialog = None
        self.unmute_browse_dialog = None
        self.mute_sound_filename = None
        self.unmute_sound_filename = None

        self.volume_level = self.parent_app.settings.setting["sound_volume"] * 100
        self.volume_label = self.findChild(QtWidgets.QLabel, 'volumeLabel')
        self.volume_label.setText(str(self.volume_level))
        self.volume_slider = self.findChild(QtWidgets.QSlider, 'volumeSlider')
        self.volume_slider.setValue(self.volume_level)
        self.volume_slider.valueChanged.connect(self.slider_cb)

        self.mute_browse_button = self.findChild(QtWidgets.QPushButton, 'muteBrowseButton')
        self.mute_browse_button.clicked.connect(self.mute_browse_button_cb)

        self.unmute_browse_button = self.findChild(QtWidgets.QPushButton, 'unmuteBrowseButton')
        self.unmute_browse_button.clicked.connect(self.unmute_browse_button_cb)

    def slider_cb(self):
        self.volume_label.setText(str(self.volume_slider.value()))
        self.volume_level = self.volume_slider.value()
        self.parent_app.settings.setting["sound_volume"] = self.volume_level / 100
        settings_util.write_settings(self.parent_app.settings)

    def mute_browse_button_cb(self):
        self.mute_browse_dialog = QtWidgets.QFileDialog()
        path = sounds_dir
        self.mute_sound_filename = QtWidgets.QFileDialog.getOpenFileName(self.mute_browse_dialog, "", path)
        if self.mute_sound_filename[0] != "" and Path(self.mute_sound_filename[0]).is_file():
            self.parent_app.settings.setting["sound_files"][0]["mute_sound"] = self.mute_sound_filename[0]
            settings_util.write_settings(self.parent_app.settings)

    def unmute_browse_button_cb(self):
        self.unmute_browse_dialog = QtWidgets.QFileDialog()
        path = sounds_dir
        self.unmute_sound_filename = QtWidgets.QFileDialog.getOpenFileName(self.mute_browse_dialog, "", path)
        if self.unmute_sound_filename[0] != "" and Path(self.unmute_sound_filename[0]).is_file():
            self.parent_app.settings.setting["sound_files"][1]["unmute_sound"] = self.unmute_sound_filename[0]
            settings_util.write_settings(self.parent_app.settings)
