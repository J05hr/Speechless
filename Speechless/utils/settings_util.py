import json
from Speechless.core import settings
from Speechless.utils import files_util


sounds_dir = files_util.get_sounds_dir()
config_dir = files_util.get_config_dir()
config_filename = files_util.get_config_dir().joinpath('config.json')
files_util.file_check(config_filename)


# defaults: (ptt mode, y key, t key, don't autorun, don't start hidden, minimize to tray,
#            enable mute sound, enable unmute sound, default sounds, 50% volume)
default_settings = settings.Settings('ptt', 'y', 't', False, False, True, True, True,
                                     [{"mute_sound": str(sounds_dir.joinpath('beep300.wav'))},
                                         {"unmute_sound": str(sounds_dir.joinpath('beep750.wav'))}], 0.5)


# try to read the last settings or fallback to defaults
def read_settings(logger):
    try:
        with open(config_filename, "r") as config_file:
            current_settings = json.load(config_file)

        mode = current_settings["mode"]
        toggle_keybinding = current_settings["toggle_keybinding"]
        ptt_keybinding = current_settings["ptt_keybinding"]
        autorun = current_settings["autorun"]
        start_hidden = current_settings["start_hidden"]
        minimize_to_tray = current_settings["minimize_to_tray"]
        enable_mute_sound = current_settings["enable_mute_sound"]
        enable_unmute_sound = current_settings["enable_unmute_sound"]
        sound_files = current_settings["sound_files"]
        # update sounds to default if None
        if current_settings["sound_files"][0]["mute_sound"] is None:
            current_settings["sound_files"][0]["mute_sound"] = str(sounds_dir.joinpath('beep300.wav'))
            write_settings(current_settings, logger)
        if current_settings["sound_files"][1]["unmute_sound"] is None:
            current_settings["sound_files"][1]["unmute_sound"] = str(sounds_dir.joinpath('beep750.wav'))
            write_settings(current_settings, logger)
        sound_volume = current_settings["sound_volume"]

        return settings.Settings(mode, toggle_keybinding, ptt_keybinding, autorun, start_hidden, minimize_to_tray,
                                 enable_mute_sound, enable_unmute_sound, sound_files, sound_volume)

    except Exception as e:
        logger.error("Error reading settings, " + str(e), exc_info=True)
        write_settings(default_settings, logger)  # fallback to defaults, overwrite the corrupted config
        return default_settings


# try to write the settings or fallback to defaults
def write_settings(new_settings, logger):
    try:
        with open(config_filename, "w") as config_file:
            json_settings = {
                "mode": new_settings.setting["mode"],
                "toggle_keybinding": new_settings.setting["toggle_keybinding"],
                "ptt_keybinding": new_settings.setting["ptt_keybinding"],
                "autorun": new_settings.setting["autorun"],
                "start_hidden": new_settings.setting["start_hidden"],
                "minimize_to_tray": new_settings.setting["minimize_to_tray"],
                "enable_mute_sound": new_settings.setting["enable_mute_sound"],
                "enable_unmute_sound": new_settings.setting["enable_unmute_sound"],
                "sound_files": new_settings.setting["sound_files"],
                "sound_volume": new_settings.setting["sound_volume"]
            }
            json.dump(json_settings, config_file)

    except Exception as e:
        logger.error("Error writing settings, " + str(e), exc_info=True)
        with open(config_filename, "w") as config_file:  # fallback to defaults
            json.dump(default_settings, config_file)
