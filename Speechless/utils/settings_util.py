from Speechless.core import settings
from pathlib import Path
import json

rel_dir = str(Path.cwd())
sounds_dir = rel_dir + '\\sounds'
config_dir = rel_dir + '\\config'
config_filename = config_dir + '\\config.json'

# defaults: (t key, autorun, don't start hidden, minimize to tray, don't show notifications,
#            play sounds, default sounds, 50% volume)
default_settings = settings.Settings(84, True, False, True, False, True,
                                     [{"mute_sound": sounds_dir+'\\beep300.wav'},
                                         {"unmute_sound": sounds_dir+'\\beep750.wav'}], 0.5)


# try to read the last settings or fallback to defaults
def read_settings():
    try:
        with open(config_filename, "r") as config_file:
            current_settings = json.load(config_file)

        keybinding = current_settings["keybinding"]
        autorun = current_settings["autorun"]
        start_hidden = current_settings["start_hidden"]
        minimize_to_tray = current_settings["minimize_to_tray"]
        show_notifications = current_settings["show_notifications"]
        play_sounds = current_settings["play_sounds"]
        sound_files = current_settings["sound_files"]
        # update sounds to default if None
        if current_settings["sound_files"][0]["mute_sound"] is None:
            current_settings["sound_files"][0]["mute_sound"] = sounds_dir + '\\beep300.wav'
            write_settings(current_settings)
        if current_settings["sound_files"][1]["unmute_sound"] is None:
            current_settings["sound_files"][1]["unmute_sound"] = sounds_dir + '\\beep750.wav'
            write_settings(current_settings)

        return settings.Settings(keybinding, autorun, start_hidden, minimize_to_tray, show_notifications,
                                 play_sounds, sound_files)

    except Exception as e:
        # print error
        print(str(e))

        # fallback to defaults, overwrite the corrupted config and return defaults
        write_settings(default_settings)
        return default_settings


# try to write the settings or fallback to defaults
def write_settings(new_settings):
    try:
        with open(config_filename, "w") as config_file:
            json_settings = {
              "keybinding": new_settings.setting["keybinding"],
              "autorun": new_settings.setting["autorun"],
              "start_hidden": new_settings.setting["start_hidden"],
              "minimize_to_tray": new_settings.setting["minimize_to_tray"],
              "show_notifications": new_settings.setting["show_notifications"],
              "play_sounds": new_settings.setting["play_sounds"],
              "sound_files": new_settings.setting["sound_files"]
            }
            json.dump(json_settings, config_file)

    except Exception as e:
        # print error
        print(str(e))

        # fallback to defaults
        with open(config_filename, "w") as config_file:
            json.dump(default_settings, config_file)
