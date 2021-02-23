import sys
from pathlib import Path
from pynput import mouse, keyboard
from PyQt5.QtWidgets import QApplication
from Speechless.core import mic_controls, mute_sanity_thread
from Speechless.gui import main_window, system_tray
from Speechless.utils import settings_util, crash_utils


class Speechless:

    def __init__(self):
        self.settings = settings_util.read_settings()
        self.rel_dir = str(Path.cwd())
        self.sounds_dir = self.rel_dir + '\\sounds'
        self.icons_dir = self.rel_dir + '\\icons'
        self.gui_app = None
        self.win = None
        self.tray = None
        self.ptt_key_pushed = False

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            # unmute if the keybinding is pressed
            self.ptt_key_pushed = True
            if str(button) == self.settings.setting['keybinding']:
                mic_controls.unmute(self, self.settings.setting["play_sounds"])
        else:
            # mute if the keybinding is released
            self.ptt_key_pushed = False
            if str(button) == self.settings.setting['keybinding']:
                mic_controls.mute(self, self.settings.setting["play_sounds"])

    def on_key_press(self, key):
        # unmute if the keybinding is pressed
        self.ptt_key_pushed = True
        if str(key) == self.settings.setting['keybinding']:
            mic_controls.unmute(self, self.settings.setting["play_sounds"])

    def on_key_release(self, key):
        self.ptt_key_pushed = False
        # mute if the keybinding is released
        if str(key) == self.settings.setting['keybinding']:
            mic_controls.mute(self, self.settings.setting["play_sounds"])

    def on_exit(self):
        # unmute on exit
        mic_controls.unmute(self, self.settings.setting["play_sounds"])

    def run(self):
        self.gui_app = QApplication(sys.argv)
        self.gui_app.aboutToQuit.connect(self.on_exit)

        self.win = main_window.MainWindow(self)
        self.tray = system_tray.SystemTrayIcon(self.icons_dir + '\\mutemic.png', self.gui_app, self.win)
        self.tray.show()

        if not self.settings.setting["start_hidden"]:
            self.win.show()

        # start muted
        mic_controls.mute(self, self.settings.setting["play_sounds"])

        # start the sanity check thread
        mst = mute_sanity_thread.MST(self)
        mst.start()

        # listen for mouse and keyboard
        m_listener = mouse.Listener(on_click=self.on_mouse_click)
        k_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        m_listener.start()
        k_listener.start()

        sys.exit(self.gui_app.exec())


if __name__ == '__main__':
    try:
        app = Speechless()
        app.run()

    except Exception as e:
        # ensure the mic is left in an un-muted state
        crash_utils.crash_unmute()
        # print error
        print("Fatal Error, " + str(e))



