import threading
import sounddevice as sd
import numpy as np


class MuteInputReadThread (threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.parent_app = app
        self.kill = False

    def get_sound_level(self, indata, o, f, t, s):
        volume_norm = np.linalg.norm(indata) * 10
        self.parent_app.input_level = int(volume_norm)

    def run(self):
        # 1 sec sleep loop to run the sanity check
        with sd.Stream(callback=self.get_sound_level):
            while not self.kill:
                sd.sleep(1)

    def stop(self):
        self.kill = True
