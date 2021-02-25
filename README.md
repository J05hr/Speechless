
# Speechless v1.0
A windows utility to enable global microphone controls and push-to-talk.


## About The Project

- Speechless is a simple application built for Windows 10 that enables system-wide microphone controls and push-to-talk functionality. 
This allows the user to enjoy a push-to-talk experience where they normally would have little or no control (i.e. web video conferencing).
- Additionally, it helps guard your privacy by enabling a default state of muted for the microphone and executes a safety loop to ensure that the microphone stays in the state you want. Microphones often go overlooked in terms or privacy and this little app allows you to prevent background eavesdropping.  


## How It Works

- The app consists of two main GUI components: a main window where settings are established, and a system-tray icon for monitoring, opening the main window, and exiting the app.
- The app consists of 4 main threads: the application thread, a key and mouse listener, an input level listener, and a safety thread to ensure the microphone state is as intended. 
- The app simply listens for your key-binding and mutes or un-mutes your mic based on your settings and current mode.


## Built With

* Programing Language: Python
* GUI Framework: PyQt5
* Third Party Libraries:
  - pywin32 for access to microphone contols
  - audioplayer for playing sounds
  - sounddevice for monitoring audio
  - pyaudio for getting devices
  - pynput for key and mouse listeners
  - pyinstaller for generating the executable


## Installation
- From this [repo](https://github.com/j05hr/Speechless) You can simply download the ```Speechless v1.0.zip``` and unzip.
- All the files in the Speechless v1.0 folder are required dependencies and this folder can be stored anywhere on your system that does not require elevated permissions.
- Now simply run the ```speechless v1.0.exe``` and establish your preferred settings.


## Usage

- Opening and Exiting:
  - To open the program simply run ```speechless v1.0.exe```. If the window is hidden you may open it from the system-tray icon.
  - To enable auto-run on start-up there is a setting under main window ```Options```, or you may manually add a shortcut to your systems startup folder.
  - Exiting the application is done exclusively through the system-tray icon by clicking the ```Quit``` option.
  - Additionally, there are settings under main window ```Options``` for starting with the main window hidden and minimizing the main window to tray.
- Modes
  - There are two main modes under main window ```Mode```. Here you can switch between PTT or Toggle modes.
  - PTT means the mic will start muted and be muted until you press the key-binding and un-muted only as long as it's held.
  - Toggle means the mic will start un-muted and be toggled between muted and un-muted each time you press the key-binding.
- Keybinding
  - Keybindings reside under main window ```Keybinding```. Here you can set single key or button bindings for both modes.
- Sounds
  - Sound settings reside under main window ```Notifications```. Here you can set custom sounds, sound levels, and which sounds to play.
## Contributing

Contributions and issues are welcome.

See the [open issues](https://github.com/j05hr/Speechless/issues) for a list of proposed features (and known issues).

1. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
2. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the Branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

If you found this code useful and want to make a donation:
- Donate BTC:  34bSjJ1vQypexeviXbSxL7tFginc9uux86
- Donate USDC: 0xf91b0a761cd37142a6afe829364551aa51fdc53e

## License

Distributed under the GPLv3 License. See `LICENSE` for more information.


## Contact

Admin - mail@j0sh.codes

Github: [https://github.com/j05hr](https://github.com/j05hr)
