from pynput import mouse, keyboard
from PyQt5 import uic, QtWidgets, QtGui
from Speechless.utils import settings_util, files_util


ptt_keybinding_window_layout_file = files_util.get_layouts_dir().joinpath('ptt_keybinding_window.ui')
files_util.file_check(ptt_keybinding_window_layout_file)
FormClass, BaseClass = uic.loadUiType(ptt_keybinding_window_layout_file)


class PttKeyBindingWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(PttKeyBindingWindow, self).__init__()
        self.setupUi(self)
        icon_filepath = files_util.get_icons_dir().joinpath('mic.png')
        files_util.file_check(icon_filepath)
        self.setWindowIcon(QtGui.QIcon(str(icon_filepath)))

        self.parent_app = app
        self.ptt_key_input_text = self.findChild(QtWidgets.QLineEdit, 'PttKeybinding')
        self.ptt_key_input_text.setText(self.parent_app.settings.setting["ptt_keybinding"])
        self.ptt_keybinding = None
        self.listen_button = self.findChild(QtWidgets.QPushButton, 'listenButton')
        self.listen_button.clicked.connect(self.listen_button_cb)
        self.save_button = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.save_button.clicked.connect(self.save_button_cb)

        self.kl = None
        self.ml = None

    def on_click(self, x, y, button, pressed):
        self.ptt_key_input_text.setText(str(button))
        self.ptt_keybinding = str(button)
        self.kl.stop()
        self.ml.stop()

    def on_press(self, key):
        key_str = str(key).strip('\'\\')
        self.ptt_key_input_text.setText(key_str)
        self.ptt_keybinding = key_str
        self.kl.stop()
        self.ml.stop()

    def listen_button_cb(self):
        self.kl = keyboard.Listener(on_press=self.on_press)
        self.ml = mouse.Listener(on_click=self.on_click)
        self.kl.start()
        self.ml.start()

    def save_button_cb(self):
        if self.ptt_keybinding:
            self.parent_app.settings.setting["ptt_keybinding"] = self.ptt_keybinding
            settings_util.write_settings(self.parent_app.settings)
            self.hide()


