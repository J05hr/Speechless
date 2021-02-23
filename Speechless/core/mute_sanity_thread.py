import time
import threading
from Speechless.core import mic_controls


class MST (threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.parent_app = app

    def mute_sanity_check_fix(self):
        # as long as the button is not pushed ensure the mic is muted in_case of external changes
        if not self.parent_app.ptt_key_pushed:
            mic_controls.mute(self.parent_app, self.parent_app.settings.setting["play_sounds"])

    def run(self):
        # 5 sec sleep loop to run the sanity check
        while True:
            time.sleep(5)
            self.mute_sanity_check_fix()
