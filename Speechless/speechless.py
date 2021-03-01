import sys
import traceback
from pynput import mouse, keyboard
from PyQt5.QtWidgets import QApplication
from Speechless.core import mic_controls, mute_sanity_thread, mic_input_read_thread
from Speechless.gui import main_window, system_tray
from Speechless.utils import settings_util, autorun_utils, files_util


class Speechless:

    def __init__(self):
        # settings
        self.settings = settings_util.read_settings()

        # states
        self.mode = self.settings.setting['mode']
        self.ptt_key_pushed = False
        self.input_level = None
        self.toggle_state = 'unmuted'

        # gui
        self.gui_app = None
        self.win = None
        self.tray = None

        # threads
        self.mst = mute_sanity_thread.MST(self)
        self.mirt = mic_input_read_thread.MIRT(self)
        self.m_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.k_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)

    def on_mouse_click(self, x, y, button, pressed):
        if self.mode == 'ptt':
            if pressed:
                # unmute if the keybinding is pressed
                if str(button) == self.settings.setting['ptt_keybinding']:
                    self.ptt_key_pushed = True
                    mic_controls.unmute(self)
            else:
                # mute if the keybinding is released
                if str(button) == self.settings.setting['ptt_keybinding']:
                    self.ptt_key_pushed = False
                    mic_controls.mute(self)
        elif self.mode == 'toggle':
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
        if self.mode == 'ptt':
            # unmute if the keybinding is pressed
            if str(key).strip('\'\\') == self.settings.setting['ptt_keybinding']:
                if not self.ptt_key_pushed:
                    self.ptt_key_pushed = True
                    mic_controls.unmute(self)
        elif self.mode == 'toggle':
            if str(key).strip('\'\\') == self.settings.setting['toggle_keybinding']:
                # toggle the mute
                if self.toggle_state == 'unmuted':
                    mic_controls.mute(self)
                    self.toggle_state = 'muted'
                else:
                    mic_controls.unmute(self)
                    self.toggle_state = 'unmuted'

    def on_key_release(self, key):
        if self.mode == 'ptt':
            # mute if the keybinding is released
            if str(key).strip('\'\\') == self.settings.setting['ptt_keybinding']:
                mic_controls.mute(self)
                self.ptt_key_pushed = False

    def on_exit(self):
        # kill any existing threads
        self.mst.stop()
        self.mst.join()
        self.mirt.stop()
        self.mirt.join()
        self.m_listener.stop()
        self.k_listener.stop()
        # ensure unmute on exit
        mic_controls.basic_unmute()

    def run(self):
        # run gui
        self.gui_app = QApplication(sys.argv)
        self.gui_app.aboutToQuit.connect(self.on_exit)
        self.win = main_window.MainWindow(self)
        icon_filepath = files_util.get_icons_dir().joinpath('mutemic.png')
        files_util.file_check(icon_filepath)
        self.tray = system_tray.SystemTrayIcon(icon_filepath, self.gui_app, self.win)
        self.tray.show()
        if not self.settings.setting["start_hidden"]:
            self.win.show()

        # add autostart if set
        autorun = self.settings.setting['autorun']
        if autorun:
            autorun_utils.add_autorun()
        else:
            autorun_utils.remove_autorun()

        # listen for mouse and keyboard
        self.m_listener.start()
        self.k_listener.start()

        # start the sanity check thread and the input reader thread
        self.mirt.start()
        self.mst.start()

        # start muted if ptt mode or un-muted if toggle mode
        if self.mode == 'ptt':
            mic_controls.mute(self)
        elif self.mode == 'toggle':
            mic_controls.unmute(self)

        sys.exit(self.gui_app.exec())


if __name__ == '__main__':
    try:
        speechless = Speechless()
        speechless.run()

    except Exception as e:
        # print error
        print("Fatal Error, " + str(e))
        traceback.print_exc()
        # ensure the mic is left in an un-muted state
        mic_controls.basic_unmute()
        # on fatal error reset the settings to default
        settings_util.write_settings(settings_util.default_settings)




