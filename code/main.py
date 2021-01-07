import sys
from PyQt5.QtWidgets import *
from Interface import Opening

if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = app.desktop()
    Window = Opening(window_size=(desktop.width(), desktop.height()))
    Window.setFocus()
    Window.show()

    app.exec_()
