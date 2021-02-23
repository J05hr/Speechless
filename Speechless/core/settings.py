

class Settings:
    def __init__(self, mode, toggle_keybinding, ptt_keybinding, autorun, start_hidden, minimize_to_tray, show_notifications,
                 play_sounds, sound_files, sound_volume):

        self.setting = {
            "mode": mode,  # the current application mode, toggle or ppt
            "toggle_keybinding": toggle_keybinding,  # current toggle keybinding, stores key code
            "ptt_keybinding": ptt_keybinding,  # current ptt keybinding, stores key string
            "autorun": autorun,   # autorun at startup, boolean
            "start_hidden": start_hidden,  # start in minimized, boolean
            "minimize_to_tray": minimize_to_tray,   # minimize to tray, boolean
            "show_notifications": show_notifications,  # show desktop notifications, boolean
            "play_sounds": play_sounds,  # play notification sounds on change, boolean
            "sound_files": sound_files,  # sound file locations for notifications, tuple of filenames (mute, unmute)
            "sound_volume": sound_volume  # sound file locations for notifications, tuple of filenames (mute, unmute)
        }
