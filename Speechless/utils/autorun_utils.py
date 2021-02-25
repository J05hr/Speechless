from pathlib import Path
from win32com import client
from win32comext.shell import shell, shellcon


rel_dir = str(Path.cwd())
app_data = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0)


# attempt to add a shortcut to the exe to the startup folder so it will autorun on startup
def add_autorun():
    try:
        target = Path(rel_dir + '/speechless.exe')
        path = Path(app_data + '/Microsoft/Windows/Start Menu/Programs/Startup/speechless.exe.lnk')
        shell = client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(path))
        shortcut.TargetPath = str(target)
        shortcut.WorkingDirectory = rel_dir
        shortcut.Save()
    except Exception as e:
        print("Failed to add startup item, " + str(e))


# attempt to remove the shortcut from the startup folder so it will not autorun on startup
def remove_autorun():
    try:
        rpath = Path(app_data + '/Microsoft/Windows/Start Menu/Programs/Startup/speechless.exe.lnk')
        rpath.unlink(missing_ok=True)
    except Exception as e:
        print("Failed to delete startup item, " + str(e))
