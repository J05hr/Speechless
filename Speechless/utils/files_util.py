from pathlib import Path


cwd = Path.cwd()
sounds_dir = cwd.joinpath('sounds')
layouts_dir = cwd.joinpath('layouts')
config_dir = cwd.joinpath('config')
icons_dir = cwd.joinpath('icons')
log_dir = cwd.joinpath('log')


def get_cwd():
    if Path.exists(cwd):
        return cwd
    else:
        raise NotADirectoryError(f"Required directory {cwd} doesn't exist")


def get_sounds_dir():
    if Path.exists(sounds_dir):
        return sounds_dir
    else:
        raise NotADirectoryError(f"Required directory {sounds_dir} doesn't exist")


def get_layouts_dir():
    if Path.exists(layouts_dir):
        return layouts_dir
    else:
        raise NotADirectoryError(f"Required directory {layouts_dir} doesn't exist")


def get_config_dir():
    if Path.exists(config_dir):
        return config_dir
    else:
        raise NotADirectoryError(f"Required directory {config_dir} doesn't exist")


def get_icons_dir():
    if Path.exists(icons_dir):
        return icons_dir
    else:
        raise NotADirectoryError(f"Required directory {icons_dir} doesn't exist")


def get_log_dir():
    if Path.exists(log_dir):
        return log_dir
    else:
        raise NotADirectoryError(f"Required directory {log_dir} doesn't exist")


def file_check(path):
    if Path.exists(path):
        return True
    else:
        raise FileExistsError(f"Required file {path} doesn't exist")
