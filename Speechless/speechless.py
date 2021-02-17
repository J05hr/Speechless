from PyQt5.QtWidgets import QApplication
from Speechless.gui import main_window
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main_window.MainWindow()
    win.show()
    sys.exit(app.exec())
