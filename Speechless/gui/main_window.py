import pyaudio
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from Speechless.core import mic_controls
from Speechless.utils import settings_util, autorun_utils, files_util
from Speechless.gui import about_window, ptt_keybinding_window, toggle_keybinding_window, custom_sounds_window


main_window_layout_file = files_util.get_layouts_dir().joinpath('main_window.ui')
files_util.file_check(main_window_layout_file)
FormClass, BaseClass = uic.loadUiType(main_window_layout_file)


class MainWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        # Setup
        self.parent_app = app
        self.setupUi(self)
        icon_filepath = files_util.get_icons_dir().joinpath('mic.png')
        files_util.file_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))

        # Windows
        self.about_win = about_window.AboutWindow()
        self.toggle_keybinding_win = toggle_keybinding_window.ToggleKeyBindingWindow(self.parent_app)
        self.ptt_keybinding_win = ptt_keybinding_window.PttKeyBindingWindow(self.parent_app)
        self.custom_sounds_win = custom_sounds_window.CustomSoundsWindow(self.parent_app)

        # Modes
        self.action_toggle_mode = self.findChild(QtWidgets.QAction, 'actionToggleMode')
        self.action_ptt_mode = self.findChild(QtWidgets.QAction, 'actionPTTMode')
        if self.parent_app.settings.setting['mode'] == 'ptt':
            self.action_ptt_mode.setChecked(True)
        else:
            self.action_toggle_mode.setChecked(True)
        self.action_toggle_mode.triggered.connect(self.toggle_mode_action_cb)
        self.action_ptt_mode.triggered.connect(self.ptt_mode_action_cb)

        # Menu Options
        self.action_toggle_keybinding = self.findChild(QtWidgets.QAction, 'actionTogglekeybinding')
        self.action_toggle_keybinding.triggered.connect(self.toggle_key_action_cb)

        self.action_ptt_keybinding = self.findChild(QtWidgets.QAction, 'actionPTTkeybinding')
        self.action_ptt_keybinding.triggered.connect(self.ptt_key_action_cb)

        self.action_auto_run = self.findChild(QtWidgets.QAction, 'actionAutorun')
        if self.parent_app.settings.setting['autorun']:
            self.action_auto_run.setChecked(True)
        self.action_auto_run.triggered.connect(self.autorun_action_cb)
        self.action_start_hidden = self.findChild(QtWidgets.QAction, 'actionStart_hidden')
        if self.parent_app.settings.setting['start_hidden']:
            self.action_start_hidden.setChecked(True)
        self.action_start_hidden.triggered.connect(self.start_hidden_action_cb)
        self.action_minimize_to_tray = self.findChild(QtWidgets.QAction, 'actionMinimize_to_tray')
        if self.parent_app.settings.setting['minimize_to_tray']:
            self.action_minimize_to_tray.setChecked(True)
        self.action_minimize_to_tray.triggered.connect(self.minimize_to_tray_action_cb)

        # Menu Notifications
        self.action_enable_mute_sound = self.findChild(QtWidgets.QAction, 'actionEnableMuteSound')
        if self.parent_app.settings.setting['enable_mute_sound']:
            self.action_enable_mute_sound.setChecked(True)
        self.action_enable_unmute_sound = self.findChild(QtWidgets.QAction, 'actionEnableUnmuteSound')
        if self.parent_app.settings.setting['enable_unmute_sound']:
            self.action_enable_unmute_sound.setChecked(True)
        self.action_enable_mute_sound.triggered.connect(self.enable_mute_sound_action_cb)
        self.action_enable_unmute_sound.triggered.connect(self.enable_unmute_sound_action_cb)
        self.action_custom_sounds = self.findChild(QtWidgets.QAction, 'actionCustom_Sounds')
        self.action_custom_sounds.triggered.connect(self.custom_sounds_action_cb)

        self.action_info = self.findChild(QtWidgets.QAction, 'actionInfo')
        self.action_info.triggered.connect(self.about_window_action_cb)

        self.menu_device = self.findChild(QtWidgets.QMenu, 'menuDevice')
        self.pa = pyaudio.PyAudio()
        self.default_input_device = self.pa.get_default_input_device_info()
        self.current_device = QtWidgets.QAction(self.default_input_device["name"])
        self.current_device.setCheckable(True)
        self.current_device.setChecked(True)
        self.current_device.setEnabled(False)
        self.menu_device.addAction(self.current_device)

    # Turn on toggle mode.
    def toggle_mode_action_cb(self):
        if self.parent_app.mode != 'toggle':
            mic_controls.unmute(self.parent_app, self.parent_app.logger)  # Start toggle mode un-muted.
            self.parent_app.mode = 'toggle'
            self.action_ptt_mode.setChecked(False)
            self.parent_app.settings.setting['mode'] = 'toggle'
            settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)
        else:
            self.action_toggle_mode.setChecked(True)

    # Turn on ptt mode.
    def ptt_mode_action_cb(self):
        if self.parent_app.mode != 'ptt':
            mic_controls.mute(self.parent_app, self.parent_app.logger)  # Start ptt mode muted.
            self.parent_app.mode = 'ptt'
            self.action_toggle_mode.setChecked(False)
            self.parent_app.settings.setting['mode'] = 'ptt'
            settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)
        else:
            self.action_ptt_mode.setChecked(True)

    # Set ptt key bindings.
    def ptt_key_action_cb(self):
        self.ptt_keybinding_win.show()

    # Set toggle key bindings.
    def toggle_key_action_cb(self):
        self.toggle_keybinding_win.show()

    # Set autorun.
    def autorun_action_cb(self):
        if self.action_auto_run.isChecked():
            self.parent_app.settings.setting['autorun'] = True
            autorun_utils.add_autorun(self.parent_app.logger)
        else:
            self.parent_app.settings.setting['autorun'] = False
            autorun_utils.remove_autorun(self.parent_app.logger)
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    # Set start hidden.
    def start_hidden_action_cb(self):
        if self.action_start_hidden.isChecked():
            self.parent_app.settings.setting['start_hidden'] = True
        else:
            self.parent_app.settings.setting['start_hidden'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    # Set start muted.
    def start_muted_action_cb(self):
        if self.action_start_muted.isChecked():
            self.parent_app.settings.setting['start_muted'] = True
        else:
            self.parent_app.settings.setting['start_muted'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    # Set minimize to tray.
    def minimize_to_tray_action_cb(self):
        if self.action_minimize_to_tray.isChecked():
            self.parent_app.settings.setting['minimize_to_tray'] = True
        else:
            self.parent_app.settings.setting['minimize_to_tray'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    # Set enable mute sound.
    def enable_mute_sound_action_cb(self):
        if self.action_enable_mute_sound.isChecked():
            self.parent_app.settings.setting['enable_mute_sound'] = True
        else:
            self.parent_app.settings.setting['enable_mute_sound'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    # Set enable unmute sound.
    def enable_unmute_sound_action_cb(self):
        if self.action_enable_unmute_sound.isChecked():
            self.parent_app.settings.setting['enable_unmute_sound'] = True
        else:
            self.parent_app.settings.setting['enable_unmute_sound'] = False
        settings_util.write_settings(self.parent_app.settings, self.parent_app.logger)

    # Set custom sounds.
    def custom_sounds_action_cb(self):
        self.custom_sounds_win.show()

    # Show about window.
    def about_window_action_cb(self):
        self.about_win.show()

    # Override minimize depending on the 'minimize to tray' setting.
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange and self.parent_app.settings.setting['minimize_to_tray']:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()

    # Override closeEvent to hide instead of quit, you must quit from the tray icon.
    def closeEvent(self, close_event):
        close_event.ignore()
        self.hide()
