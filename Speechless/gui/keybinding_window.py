from pathlib import Path
from pynput import mouse, keyboard
from PyQt5 import uic, QtWidgets
from Speechless.utils import settings_util


FormClass, BaseClass = uic.loadUiType(str(Path.cwd()) + '\\layouts\\keybinding_window.ui')


class KeyBindingWindow(BaseClass, FormClass):
    def __init__(self, app):
        super(KeyBindingWindow, self).__init__()
        self.setupUi(self)

        self.parent_app = app
        self.key_input_text = self.findChild(QtWidgets.QLineEdit, 'Keybinding')
        self.key_input_text.setText(self.parent_app.settings.setting["keybinding"])
        self.keybinding = None
        self.listen_button = self.findChild(QtWidgets.QPushButton, 'listenButton')
        self.listen_button.clicked.connect(self.listen_button_cb)
        self.save_button = self.findChild(QtWidgets.QPushButton, 'saveButton')
        self.save_button.clicked.connect(self.save_button_cb)

        self.kl = None
        self.ml = None

    def on_click(self, x, y, button, pressed):
        self.key_input_text.setText(str(button))
        self.keybinding = str(button)
        self.kl.stop()
        self.ml.stop()

    def on_press(self, key):
        self.key_input_text.setText(str(key))
        self.keybinding = str(key)
        self.kl.stop()
        self.ml.stop()

    def listen_button_cb(self):
        self.kl = keyboard.Listener(on_press=self.on_press)
        self.ml = mouse.Listener(on_click=self.on_click)
        self.kl.start()
        self.ml.start()

    def save_button_cb(self):
        if self.keybinding:
            self.parent_app.settings.setting["keybinding"] = self.keybinding
            settings_util.write_settings(self.parent_app.settings)
            self.hide()


