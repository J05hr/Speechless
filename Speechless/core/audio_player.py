from ctypes import windll


class PlayerError(Exception):
    """Basic exception for errors raised by Player"""
    pass


class Player:

    def __init__(self, filepath):
        self.alias = str(id(self))               # assign an alias as a reference to the player
        self.filepath = filepath             # The file name as provided
        self.volume = 100                    # start the volume at 100%
        self.load_player()                   # load the player

    def __del__(self):
        self.close()

    def mci_send_string(self, command):
        # print("alias: " + self.alias)
        return windll.winmm.mciSendStringW(command, None, 0, 0)

    def get_filename(self):
        return self.filepath

    def get_volume(self):
        return self.volume

    def set_volume(self, value):
        value = max(min(value, 100), 0)  # clamp to [0..100]
        self.volume = int(value * 10)  # MCI volume: 0...1000
        ret = self.mci_send_string('setaudio {} volume to {}'.format(self.alias, self.volume))
        # print("vol: " + str(ret))
        if ret != 0:
            raise PlayerError('Failed to set_volume for alias "{}"'.format(self.alias))

    def load_player(self):
        ret = self.mci_send_string('open "{}" type mpegvideo alias {}'.format(self.filepath, self.alias))
        # print("load: " + str(ret))
        if ret != 0 and ret != 289:
            raise PlayerError('Failed to load player for "{}"'.format(self.filepath))
        return ret

    def play(self, loop=False, block=False):
        """
        Starts audio playback.
            - loop:  bool – Sets whether to repeat the track automatically when finished.
            - block: bool – If true, blocks the thread until playback ends.
        """
        sloop = 'repeat' if loop else ''
        swait = 'wait' if block else ''
        ret = self.mci_send_string('play {} from 0 {} {}'.format(self.alias, sloop, swait))
        # print("play: " + str(ret))
        if ret != 0:
            raise PlayerError('Failed to play alias "{}"'.format(self.alias))

    def close(self):
        """
        Closes device, releasing resources. Can't play again.
        """
        ret = self.mci_send_string('close {}'.format(self.alias))
        # print('close: ' + str(ret))