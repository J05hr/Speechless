import playsound
import win32api
import win32gui
from PyQt5 import QtGui
from Speechless.utils import settings_util

current_settings = settings_util.read_settings()
WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a * 0x10000
APPCOMMAND_MICROPHONE_VOLUME_DOWN = 0x19 * 0x10000


# mute if not muted
def mute(app, play_sounds):
    app.tray.setIcon(QtGui.QIcon(app.icons_dir + '\\mutemic.png'))
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
    # play unmute sound
    if play_sounds:
        playsound.playsound(current_settings.setting["sound_files"][0]["mute_sound"])


# unmute if not unmuted
def unmute(app, play_sounds):
    app.tray.setIcon(QtGui.QIcon(app.icons_dir + '\\unmutemic.png'))
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    # play unmute sound
    if play_sounds:
        playsound.playsound(current_settings.setting["sound_files"][1]["unmute_sound"])
