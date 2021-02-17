from PyQt5 import uic
from PyQt5.QtWidgets import *
from pathlib import Path
from Speechless.gui import about_window


reldir = str(Path.cwd())
FormClass, BaseClass = uic.loadUiType(reldir + '\\layouts\\main_window.ui')


class MainWindow(BaseClass, FormClass):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.about_win = about_window.AboutWindow()
        self.setupUi(self)

        self.global_mute_radio_button = self.findChild(QRadioButton, 'globalMuteRadioButton')
        self.global_mute_radio_button.toggled.connect(self.gm_button_cb)

        self.push_to_talk_radio_button = self.findChild(QRadioButton, 'pushToTalkRadioButton')
        self.push_to_talk_radio_button.toggled.connect(self.ptt_button_cb)

        # menu options
        self.action_keybinding = self.findChild(QAction, 'actionKeybinding')
        self.action_keybinding.triggered.connect(self.key_action_cb)
        self.action_auto_run = self.findChild(QAction, 'actionAutorun')
        self.action_auto_run.triggered.connect(self.ar_action_cb)
        self.action_start_muted = self.findChild(QAction, 'actionStart_muted')
        self.action_start_muted.triggered.connect(self.sm_action_cb)
        self.action_minimize_to_tray = self.findChild(QAction, 'actionMinimize_to_tray')
        self.action_minimize_to_tray.triggered.connect(self.mtt_action_cb)


        # menu notifications
        self.action_show_notifications = self.findChild(QAction, 'actionShow_Notifications')
        self.action_show_notifications.triggered.connect(self.sn_action_cb)
        self.action_play_sounds = self.findChild(QAction, 'actionPlay_Sounds')
        self.action_play_sounds.triggered.connect(self.ps_action_cb)
        self.action_custom_sounds = self.findChild(QAction, 'actionCustom_Sounds')
        self.action_custom_sounds.triggered.connect(self.cs_action_cb)

        self.action_info = self.findChild(QAction, 'actionInfo')
        self.action_info.triggered.connect(self.ab_action_cb)

        self.menu_devices = self.findChild(QMenu, 'menuDevices')

    # global mute
    def gm_button_cb(self):
        pass

    # push to talk
    def ptt_button_cb(self):
        pass

    # set key bindings
    def key_action_cb(self):
        pass

    # set autorun
    def ar_action_cb(self):
        pass

    # set start muted
    def sm_action_cb(self):
        pass

    # set minimize to tray
    def mtt_action_cb(self):
        pass

    # set show notifications
    def sn_action_cb(self):
        pass

    # set play sounds
    def ps_action_cb(self):
        pass

    # set custom sounds
    def cs_action_cb(self):
        pass

    # show about window
    def ab_action_cb(self):
        self.about_win.show()
