import win32api
import win32gui
import traceback
from PyQt5 import QtGui
from audioplayer import AudioPlayer


WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a * 0x10000
APPCOMMAND_MICROPHONE_VOLUME_DOWN = 0x19 * 0x10000


# mute if not muted
def mute(app):
    current_settings = app.settings
    app.tray.setIcon(QtGui.QIcon(app.icons_dir + '\\mutemic.png'))
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
    # play unmute sound
    if current_settings.setting["enable_mute_sound"]:
        try:
            app.mute_sound = AudioPlayer(current_settings.setting["sound_files"][0]["mute_sound"])
            app.mute_sound.volume = int(current_settings.setting["sound_volume"] * 100)
            app.mute_sound.play(block=False)
        except Exception as e:
            # print error
            print("Error Playing Mute Sound, " + str(e))
            traceback.print_exc()


# unmute if not un-muted
def unmute(app):
    current_settings = app.settings
    app.tray.setIcon(QtGui.QIcon(app.icons_dir + '\\unmutemic.png'))
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
    # play unmute sound
    if current_settings.setting["enable_unmute_sound"]:
        try:
            app.unmute_sound = AudioPlayer(current_settings.setting["sound_files"][1]["unmute_sound"])
            app.unmute_sound.volume = int(current_settings.setting["sound_volume"] * 100)
            app.unmute_sound.play(block=False)
        except Exception as e:
            # print error
            print("Error Playing Un-mute Sound, " + str(e))
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
