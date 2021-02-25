from Speechless.core import settings
from pathlib import Path
import json

rel_dir = str(Path.cwd())
sounds_dir = rel_dir + '\\sounds'
config_dir = rel_dir + '\\config'
config_filename = config_dir + '\\config.json'

# defaults: (ptt mode, y key, t key, don't autorun, don't start hidden, minimize to tray, don't show notifications,
#            enable mute sound, enable unmute sound, default sounds, 50% volume)
default_settings = settings.Settings('ptt', 'y', 't', False, False, True, False, True, True,
                                     [{"mute_sound": sounds_dir+'\\beep300.wav'},
                                         {"unmute_sound": sounds_dir+'\\beep750.wav'}], 0.5)


# try to read the last settings or fallback to defaults
def read_settings():
    try:
        with open(config_filename, "r") as config_file:
            current_settings = json.load(config_file)

        mode = current_settings["mode"]
        toggle_keybinding = current_settings["toggle_keybinding"]
        ptt_keybinding = current_settings["ptt_keybinding"]
        autorun = current_settings["autorun"]
        start_hidden = current_settings["start_hidden"]
        minimize_to_tray = current_settings["minimize_to_tray"]
        show_notifications = current_settings["show_notifications"]
        enable_mute_sound = current_settings["enable_mute_sound"]
        enable_unmute_sound = current_settings["enable_unmute_sound"]
        sound_files = current_settings["sound_files"]
        # update sounds to default if None
        if current_settings["sound_files"][0]["mute_sound"] is None:
            current_settings["sound_files"][0]["mute_sound"] = sounds_dir + '\\beep300.wav'
            write_settings(current_settings)
        if current_settings["sound_files"][1]["unmute_sound"] is None:
            current_settings["sound_files"][1]["unmute_sound"] = sounds_dir + '\\beep750.wav'
            write_settings(current_settings)
        sound_volume = current_settings["sound_volume"]

        return settings.Settings(mode, toggle_keybinding, ptt_keybinding, autorun, start_hidden, minimize_to_tray,
                                 show_notifications, enable_mute_sound, enable_unmute_sound, sound_files, sound_volume)

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
                "mode": new_settings.setting["mode"],
                "toggle_keybinding": new_settings.setting["toggle_keybinding"],
                "ptt_keybinding": new_settings.setting["ptt_keybinding"],
                "autorun": new_settings.setting["autorun"],
                "start_hidden": new_settings.setting["start_hidden"],
                "minimize_to_tray": new_settings.setting["minimize_to_tray"],
                "show_notifications": new_settings.setting["show_notifications"],
                "enable_mute_sound": new_settings.setting["enable_mute_sound"],
                "enable_unmute_sound": new_settings.setting["enable_unmute_sound"],
                "sound_files": new_settings.setting["sound_files"],
                "sound_volume": new_settings.setting["sound_volume"]
            }
            json.dump(json_settings, config_file)

    except Exception as e:
        # print error
        print(str(e))

        # fallback to defaults
        with open(config_filename, "w") as config_file:
            json.dump(default_settings, config_file)
