import win32api
import win32gui
import traceback
from PyQt5 import QtGui
from Speechless.utils import files_util
from Speechless.core import sound_output_thread


WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a * 0x10000
APPCOMMAND_MICROPHONE_VOLUME_DOWN = 0x19 * 0x10000


# mute if not muted
def mute(app):
    icon_filepath = files_util.get_icons_dir().joinpath('mutemic.png')
    files_util.file_check(icon_filepath)
    app.tray.setIcon(QtGui.QIcon(str(icon_filepath)))
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
    if app.settings.setting["enable_mute_sound"]:
        # play mute sound
        try:
            sound_output_thread.SOT(
                app.settings.setting["sound_files"][0]["mute_sound"],
                int(app.settings.setting["sound_volume"] * 100)
            ).start()
        except Exception as s_e:
            # print error
            print("Error Playing Mute Sound, " + str(s_e))
            traceback.print_exc()


# unmute if not un-muted
def unmute(app):
    icon_filepath = files_util.get_icons_dir().joinpath('unmutemic.png')
    files_util.file_check(icon_filepath)
    app.tray.setIcon(QtGui.QIcon(str(icon_filepath)))
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    if app.settings.setting["enable_unmute_sound"]:
        # play unmute sound
        try:
            sound_output_thread.SOT(
                app.settings.setting["sound_files"][1]["unmute_sound"],
                int(app.settings.setting["sound_volume"] * 100)
            ).start()
        except Exception as s_e:
            # print error
            print("Error Playing Unmute Sound, " + str(s_e))
            traceback.print_exc()


def basic_unmute():
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)


def basic_mute():
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
