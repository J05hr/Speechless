from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets
from pathlib import Path
from Speechless.gui import about_window, keybinding_window, custom_sounds_window
from Speechless.utils import settings_util
import pyaudio


FormClass, BaseClass = uic.loadUiType(str(Path.cwd()) + '\\layouts\\main_window.ui')


class MainWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.parent_app = app
        self.setupUi(self)

        self.about_win = about_window.AboutWindow()
        self.keybinding_win = keybinding_window.KeyBindingWindow(app)
        self.custom_sounds_win = custom_sounds_window.CustomSoundsWindow(app)

        self.mute_sound_filename = self.parent_app.settings.setting['sound_files'][0]['mute_sound']
        self.unmute_sound_filename = self.parent_app.settings.setting['sound_files'][1]['unmute_sound']

        # menu options
        self.action_keybinding = self.findChild(QtWidgets.QAction, 'actionKeybinding')
        self.action_keybinding.triggered.connect(self.key_action_cb)
        self.action_auto_run = self.findChild(QtWidgets.QAction, 'actionAutorun')
        if self.parent_app.settings.setting['autorun']:
            self.action_auto_run.setChecked(True)
        self.action_auto_run.triggered.connect(self.ar_action_cb)
        self.action_start_hidden = self.findChild(QtWidgets.QAction, 'actionStart_hidden')
        if self.parent_app.settings.setting['start_hidden']:
            self.action_start_hidden.setChecked(True)
        self.action_start_hidden.triggered.connect(self.sh_action_cb)
        self.action_minimize_to_tray = self.findChild(QtWidgets.QAction, 'actionMinimize_to_tray')
        if self.parent_app.settings.setting['minimize_to_tray']:
            self.action_minimize_to_tray.setChecked(True)
        self.action_minimize_to_tray.triggered.connect(self.mtt_action_cb)

        # menu notifications
        self.action_show_notifications = self.findChild(QtWidgets.QAction, 'actionShow_Notifications')
        if self.parent_app.settings.setting['show_notifications']:
            self.action_show_notifications.setChecked(True)
        self.action_show_notifications.triggered.connect(self.sn_action_cb)
        self.action_play_sounds = self.findChild(QtWidgets.QAction, 'actionPlay_Sounds')
        if self.parent_app.settings.setting['play_sounds']:
            self.action_play_sounds.setChecked(True)
        self.action_play_sounds.triggered.connect(self.ps_action_cb)
        self.action_custom_sounds = self.findChild(QtWidgets.QAction, 'actionCustom_Sounds')
        self.action_custom_sounds.triggered.connect(self.cs_action_cb)

        self.action_info = self.findChild(QtWidgets.QAction, 'actionInfo')
        self.action_info.triggered.connect(self.ab_action_cb)

        self.menu_device = self.findChild(QtWidgets.QMenu, 'menuDevice')
        self.pa = pyaudio.PyAudio()
        self.default_input_device = self.pa.get_default_input_device_info()
        self.current_device = QtWidgets.QAction(self.default_input_device["name"])
        self.current_device.setCheckable(True)
        self.current_device.setChecked(True)
        self.current_device.setEnabled(False)
        self.menu_device.addAction(self.current_device)

    # set key bindings
    def key_action_cb(self):
        self.keybinding_win.show()

    # set autorun
    def ar_action_cb(self):
        if self.action_auto_run.isChecked():
            self.parent_app.settings.setting['autorun'] = True
        else:
            self.parent_app.settings.setting['autorun'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set start hidden
    def sh_action_cb(self):
        if self.action_start_hidden.isChecked():
            self.parent_app.settings.setting['start_hidden'] = True
        else:
            self.parent_app.settings.setting['start_hidden'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set start muted
    def sm_action_cb(self):
        if self.action_start_muted.isChecked():
            self.parent_app.settings.setting['start_muted'] = True
        else:
            self.parent_app.settings.setting['start_muted'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set minimize to tray
    def mtt_action_cb(self):
        if self.action_minimize_to_tray.isChecked():
            self.parent_app.settings.setting['minimize_to_tray'] = True
        else:
            self.parent_app.settings.setting['minimize_to_tray'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set show notifications
    def sn_action_cb(self):
        if self.action_show_notifications.isChecked():
            self.parent_app.settings.setting['show_notifications'] = True
        else:
            self.parent_app.settings.setting['show_notifications'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set play sounds
    def ps_action_cb(self):
        if self.action_play_sounds.isChecked():
            self.parent_app.settings.setting['play_sounds'] = True
        else:
            self.parent_app.settings.setting['play_sounds'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set custom sounds
    def cs_action_cb(self):
        self.custom_sounds_win.show()

    # show about window
    def ab_action_cb(self):
        self.about_win.show()

    # Override minimize depending on the 'minimize to tray' setting.
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange and self.parent_app.settings.setting['minimize_to_tray']:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()

    # Override closeEvent to hide instead of quit, you must quit from the tray icon
    def closeEvent(self, close_event):
        close_event.ignore()
        self.hide()
