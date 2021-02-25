from pathlib import Path
from pynput import mouse, keyboard
from PyQt5 import uic, QtWidgets, QtGui
from Speechless.utils import settings_util


FormClass, BaseClass = uic.loadUiType(str(Path.cwd()) + '\\layouts\\toggle_keybinding_window.ui')


class ToggleKeyBindingWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(ToggleKeyBindingWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(app.icons_dir + '\\mic.png'))

        self.parent_app = app
        self.toggle_key_input_text = self.findChild(QtWidgets.QLineEdit, 'ToggleKeybinding')
        self.toggle_key_input_text.setText(self.parent_app.settings.setting["toggle_keybinding"])
        self.toggle_keybinding = None
        self.listen_button = self.findChild(QtWidgets.QPushButton, 'listenButton')
        self.listen_button.clicked.connect(self.listen_button_cb)
        self.save_button = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.save_button.clicked.connect(self.save_button_cb)

        self.kl = None
        self.ml = None

    def on_click(self, x, y, button, pressed):
        self.toggle_key_input_text.setText(str(button))
        self.toggle_keybinding = str(button)
        self.kl.stop()
        self.ml.stop()

    def on_press(self, key):
        key_str = str(key).strip('\'\\')
        self.toggle_key_input_text.setText(key_str)
        self.toggle_keybinding = key_str
        self.kl.stop()
        self.ml.stop()

    def listen_button_cb(self):
        self.kl = keyboard.Listener(on_press=self.on_press)
        self.ml = mouse.Listener(on_click=self.on_click)
        self.kl.start()
        self.ml.start()

    def save_button_cb(self):
        if self.toggle_keybinding:
            self.parent_app.settings.setting["toggle_keybinding"] = self.toggle_keybinding
            settings_util.write_settings(self.parent_app.settings)
            self.hide()


