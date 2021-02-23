import win32api
import win32gui

WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_UP = 0x1a * 0x10000
APPCOMMAND_MICROPHONE_VOLUME_DOWN = 0x19 * 0x10000


# unmute on crash utility
def crash_unmute():
    # win32 app command
    hwnd_active = win32gui.GetForegroundWindow()
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_DOWN)
    win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_UP)
