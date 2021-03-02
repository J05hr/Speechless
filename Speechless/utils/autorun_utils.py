from pathlib import Path
from win32com import client
from win32comext.shell import shell, shellcon
from Speechless.utils import files_util


app_data = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)


# attempt to add a shortcut to the exe to the startup folder so it will autorun on startup
def add_autorun(logger):
    try:
        target = files_util.get_cwd().joinpath('speechless.exe')
        path = Path(app_data + '/Microsoft/Windows/Start Menu/Programs/Startup/speechless.exe.lnk')
        shll = client.Dispatch('WScript.Shell')
        shortcut = shll.CreateShortCut(str(path))
        shortcut.TargetPath = str(target)
        shortcut.WorkingDirectory = str(files_util.get_cwd())
        shortcut.Save()
    except Exception as e:
        logger.error("Failed to add startup item, " + str(e), exc_info=True)


# attempt to remove the shortcut from the startup folder so it will not autorun on startup
def remove_autorun(logger):
    try:
        rpath = Path(app_data + '/Microsoft/Windows/Start Menu/Programs/Startup/speechless.exe.lnk')
        rpath.unlink(missing_ok=True)
    except Exception as e:
        logger.error("Failed to delete startup item, " + str(e), exc_info=True)
