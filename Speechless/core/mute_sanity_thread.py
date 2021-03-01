import time
import threading

from Speechless.core import mic_controls


class MST (threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.p_app = app
        self.kill = False

    def mute_sanity_check_fix(self):
        mode = self.p_app.settings.setting['mode']
        if mode == 'ptt':
            # as long as the button is not pushed ensure the mic is muted in_case of external changes
            if not self.p_app.ptt_key_pushed and self.p_app.input_level > 0:
                mic_controls.basic_mute()
        elif mode == 'toggle':
            if self.p_app.toggle_state == 'muted' and self.p_app.input_level > 0:
                mic_controls.basic_mute()
            elif self.p_app.toggle_state == 'unmuted' and self.p_app.input_level == 0:
                mic_controls.basic_unmute()

    def run(self):
        # 1 sec sleep loop to run the sanity check
        while not self.kill:
            time.sleep(1)
            self.mute_sanity_check_fix()

    def stop(self):
        self.kill = True
