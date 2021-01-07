from typing import List
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from player import Player


class PressableLabel(QLabel):
    signal = pyqtSignal(Player)
    slot = pyqtSlot(Player)

    def __init__(self, window, imagePath: str = None, slot=None,
                 position: List[int] = [None, None], size: List[int] = [None, None]):
        super(PressableLabel, self).__init__(window)
        # [1]: Define image
        if imagePath is not None:
            self.pixmap = QPixmap(imagePath)
            self.setPixmap(self.pixmap)

        if None not in position:
            self.move(position[0], position[1])

        if None not in size:
            self.setFixedSize(size[0], size[1])
        self.setScaledContents(True)

        # [2]: Controlling attribute
        self.isPressed: bool = False
        self.imagePath = imagePath

        # [3]: Connecting button
        self.button = QPushButton()
        if slot is not None:
            self.button.pressed.connect(slot)
        self.button.show()

    def setImage(self, imagePath: str):
        if imagePath is not None:
            self.pixmap = QPixmap(imagePath)
            self.setPixmap(self.pixmap)

    def setPosition(self, position: List[int] = [None, None]):
        if None not in position:
            self.move(position[0], position[1])

    def setSize(self, size: List[int]):
        if None not in size:
            self.setFixedSize(size[0], size[1])

    def setSlot(self, slot):
        if slot is not None:
            self.button.pressed.connect(slot)


class CustomizedButton(QPushButton):
    def __init__(self, window, iconPath: str = None, hoveringIcon: str = None, iconSize: List[int] = [None, None],
                 position: List[int] = [None, None]):
        super(CustomizedButton, self).__init__(window)
        # [1]: Defined initial state
        # if iconPath is not None:
        #     self.setIcon(QIcon(iconPath))
        if None not in iconSize:
            self.setIconSize(QSize(iconSize[0], iconSize[1]))
        if None not in iconSize and None not in position:
            self.setGeometry(position[0], position[1], iconSize[0], iconSize[1])

        self.default_icon = iconPath
        self.hovering_icon = hoveringIcon
        self.icon_size = iconSize
        # [2]: Setup Configuration
        self.setEnabled(True)
        self.setMouseTracking(True)
        self.setUpdatesEnabled(True)
        self.ensurePolished()
        self.setFlat(False)
        self.setAutoFillBackground(False)

        self.hovering_style = "image: url('{}'); width: {}px; height: {}px; border-style: outset; " \
                         "background-repeat: no-repeat".format(self.hovering_icon, self.icon_size[0], self.icon_size[1])
        self.default_style = "image: url('{}'); width: {}px; height: {}px; border-style: outset; " \
                         "background-repeat: no-repeat".format(self.default_icon, self.icon_size[0], self.icon_size[1])
        self.style = ":hover {" + self.hovering_style + "} *{" + self.default_style + "}"
        self.setStyleSheet(self.style)
