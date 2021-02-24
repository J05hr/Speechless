import sys
import traceback
from pathlib import Path
from pynput import mouse, keyboard
from PyQt5.QtWidgets import QApplication
from Speechless.core import mic_controls, mute_sanity_thread
from Speechless.gui import main_window, system_tray
from Speechless.utils import settings_util


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
        self.toggle_state = 'unmuted'

    def on_mouse_click(self, x, y, button, pressed):
        mode = self.settings.setting['mode']
        if mode == 'ptt':
            if pressed:
                # unmute if the keybinding is pressed
                if str(button) == self.settings.setting['ptt_keybinding']:
                    mic_controls.unmute(self)
                self.ptt_key_pushed = True
            else:
                # mute if the keybinding is released
                if str(button) == self.settings.setting['ptt_keybinding']:
                    mic_controls.mute(self)
                self.ptt_key_pushed = False
        else:
            if pressed:
                if str(button) == self.settings.setting['toggle_keybinding']:
                    # toggle the mute
                    if self.toggle_state == 'unmuted':
                        mic_controls.mute(self)
                        self.toggle_state = 'muted'
                    else:
                        mic_controls.unmute(self)
                        self.toggle_state = 'unmuted'

    def on_key_press(self, key):
        mode = self.settings.setting['mode']
        if mode == 'ptt':
            # unmute if the keybinding is pressed
            key_str = str(key).strip('\'\\')
            if key_str == self.settings.setting['ptt_keybinding']:
                if not self.ptt_key_pushed:
                    mic_controls.unmute(self)
            self.ptt_key_pushed = True
        else:
            key_str = str(key).strip('\'\\')
            if key_str == self.settings.setting['toggle_keybinding']:
                # toggle the mute
                if self.toggle_state == 'unmuted':
                    mic_controls.mute(self)
                    self.toggle_state = 'muted'
                else:
                    mic_controls.unmute(self)
                    self.toggle_state = 'unmuted'

    def on_key_release(self, key):
        mode = self.settings.setting['mode']
        if mode == 'ptt':
            # mute if the keybinding is released
            key_str = str(key).strip('\'\\')
            if key_str == self.settings.setting['ptt_keybinding']:
                mic_controls.mute(self)
            self.ptt_key_pushed = False

    def on_exit(self):
        # unmute on exit
        mic_controls.unmute(self)

    def run(self):
        self.gui_app = QApplication(sys.argv)
        self.gui_app.aboutToQuit.connect(self.on_exit)

        self.win = main_window.MainWindow(self)
        self.tray = system_tray.SystemTrayIcon(self.icons_dir + '\\mutemic.png', self.gui_app, self.win)
        self.tray.show()

        if not self.settings.setting["start_hidden"]:
            self.win.show()

        # start muted if ptt mode or un-muted if toggle mode
        mode = self.settings.setting['mode']
        if mode == 'ptt':
            mic_controls.mute(self)
        else:
            mic_controls.unmute(self)

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
        mic_controls.basic_unmute()
        # print error
        print("Fatal Error, " + str(e))
        traceback.print_exc()



