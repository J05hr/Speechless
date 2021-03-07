import threading
from Speechless.core import audio_player


class SoundOutputThread (threading.Thread):
    """Establishes a thread to output notification sounds."""

    def __init__(self, filename, volume):
        threading.Thread.__init__(self)
        self.filename = filename
        self.volume = volume

    def play_sound(self):
        """Creates a new Player object, sets the volume level, and plays the sound for this threads filename."""
        player = audio_player.Player(self.filename)
        player.set_volume(self.volume)
        player.play(block=True)

    def run(self):
        """Runs the play_sound function once."""
        self.play_sound()
