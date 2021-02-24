import pyaudio
from pathlib import Path
from PyQt5 import uic, QtCore, QtWidgets
from Speechless.core import mic_controls
from Speechless.utils import settings_util
from Speechless.gui import about_window, ptt_keybinding_window, toggle_keybinding_window, custom_sounds_window


FormClass, BaseClass = uic.loadUiType(str(Path.cwd()) + '\\layouts\\main_window.ui')


class MainWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.parent_app = app
        self.setupUi(self)

        # windows
        self.about_win = about_window.AboutWindow()
        self.toggle_keybinding_win = toggle_keybinding_window.ToggleKeyBindingWindow(app)
        self.ptt_keybinding_win = ptt_keybinding_window.PttKeyBindingWindow(app)
        self.custom_sounds_win = custom_sounds_window.CustomSoundsWindow(app)

        # modes
        self.action_toggle_mode = self.findChild(QtWidgets.QAction, 'actionToggleMode')
        self.action_ptt_mode = self.findChild(QtWidgets.QAction, 'actionPTTMode')
        if self.parent_app.settings.setting['mode'] == 'ptt':
            self.action_ptt_mode.setChecked(True)
        else:
            self.action_toggle_mode.setChecked(True)
        self.action_toggle_mode.triggered.connect(self.toggle_mode_action_cb)
        self.action_ptt_mode.triggered.connect(self.ptt_mode_action_cb)

        # menu options
        self.action_toggle_keybinding = self.findChild(QtWidgets.QAction, 'actionTogglekeybinding')
        self.action_toggle_keybinding.triggered.connect(self.toggle_key_action_cb)

        self.action_ptt_keybinding = self.findChild(QtWidgets.QAction, 'actionPTTkeybinding')
        self.action_ptt_keybinding.triggered.connect(self.ptt_key_action_cb)

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
        self.action_enable_mute_sound = self.findChild(QtWidgets.QAction, 'actionEnableMuteSound')
        if self.parent_app.settings.setting['enable_mute_sound']:
            self.action_enable_mute_sound.setChecked(True)
        self.action_enable_unmute_sound = self.findChild(QtWidgets.QAction, 'actionEnableUnmuteSound')
        if self.parent_app.settings.setting['enable_unmute_sound']:
            self.action_enable_unmute_sound.setChecked(True)
        self.action_enable_mute_sound.triggered.connect(self.ems_action_cb)
        self.action_enable_unmute_sound.triggered.connect(self.eus_action_cb)
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

    # mode toggling
    def toggle_mode_action_cb(self):
        self.action_ptt_mode.setChecked(False)
        self.parent_app.settings.setting['mode'] = 'toggle'
        settings_util.write_settings(self.parent_app.settings)
        # start toggle mode un-muted
        mic_controls.unmute(self.parent_app)

    # mode toggling
    def ptt_mode_action_cb(self, mode):
        self.action_toggle_mode.setChecked(False)
        self.parent_app.settings.setting['mode'] = 'ptt'
        settings_util.write_settings(self.parent_app.settings)
        # start ptt mode umuted
        mic_controls.mute(self.parent_app)

    # set ptt key bindings
    def ptt_key_action_cb(self):
        self.ptt_keybinding_win.show()

    # set toggle key bindings
    def toggle_key_action_cb(self):
        self.toggle_keybinding_win.show()

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

    # set enable mute sound
    def ems_action_cb(self):
        if self.action_enable_mute_sound.isChecked():
            self.parent_app.settings.setting['enable_mute_sound'] = True
        else:
            self.parent_app.settings.setting['enable_mute_sound'] = False
        settings_util.write_settings(self.parent_app.settings)

    # set enable unmute sound
    def eus_action_cb(self):
        if self.action_enable_unmute_sound.isChecked():
            self.parent_app.settings.setting['enable_unmute_sound'] = True
        else:
            self.parent_app.settings.setting['enable_unmute_sound'] = False
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
