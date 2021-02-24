import time
import threading
from Speechless.core import mic_controls


class MST (threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.parent_app = app

    def mute_sanity_check_fix(self):
        mode = self.parent_app.settings.setting['mode']
        if mode == 'ptt':
            # as long as the button is not pushed ensure the mic is muted in_case of external changes
            if not self.parent_app.ptt_key_pushed:
                mic_controls.basic_mute()
        else:
            if self.parent_app.toggle_state == 'muted':
                mic_controls.basic_mute()
            else:
                mic_controls.basic_unmute()

    def run(self):
        # 5 sec sleep loop to run the sanity check
        while True:
            time.sleep(5)
            self.mute_sanity_check_fix()
