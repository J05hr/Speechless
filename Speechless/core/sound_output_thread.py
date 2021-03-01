import threading
from Speechless.core import audio_player


class SOT (threading.Thread):

    def __init__(self, filename, volume):
        threading.Thread.__init__(self)
        self.filename = filename
        self.volume = volume

    def play_sound(self):
        player = audio_player.Player(self.filename)
        player.set_volume(self.volume)
        player.play(block=True)

    def run(self):
        self.play_sound()
