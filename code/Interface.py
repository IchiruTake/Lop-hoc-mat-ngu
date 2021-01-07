""" This interface will determine the image as player's Symbol
    PyQt5 building"""

from typing import Tuple, Union
from CustomizedObject import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from player import Player
from GameLogic import GameLogic
from numpy.random import choice
from config import *


class Opening(QMainWindow):
    signal = pyqtSignal(str)
    windowWidth = 936
    windowHeight = 523

    DURATION: int = 25  # DURATION: in seconds
    CLOCK_UPDATE_SPEED: int = 1000  # CLOCK_UPDATE_SPEED: in miliseconds

    DICE_ROLLING_SPEED: int = 50    # DICE_ROLLING_SPEED: in miliseconds
    DICE_STOPPING_TIME: int = 3     # DICE_STOPPING_TIME: in seconds

    HONORING_TIME_SPEED: int = 3000  # HONORING_TIME_SPEED: in miliseconds

    COEF_DISTANCE_X = 46.5
    COEF_DISTANCE_Y = 47.25
    BASIC_POSITION = [88, 90]
    DISTANCE_PER_CM = 56

    def __init__(self, power: float = 1, window_size: Tuple[int, int] = (1920, 1080),
                 *args, **kwargs):
        super(Opening, self).__init__(*args, **kwargs)

        self.initializeUI(power=power, window_size=window_size)

    def initializeUI(self, power: float = 1, window_size: Tuple[int, int] = (1920, 1080)):
        # [1]: Declaration and setup
        self.opening_power = power
        self.max_width, self.max_height = window_size[0], window_size[1]
        self.ensurePolished()
        self.setMouseTracking(True)
        self.setUpdatesEnabled(True)

        # [2]: Make the main Window
        self.setFont(QFont("Times New Roman", int(20 * self.opening_power)))
        self.setWindowIcon(QIcon('resources/icon.ico'))
        self.setWindowTitle("Comet Class (2018/2020) - Server Launcher")
        self.setFixedSize(int(self.windowWidth * self.opening_power), int(self.windowHeight * self.opening_power))
        self.setEnabled(True)
        self.setMouseTracking(True)

        # [3]: Setting openingImage
        self.openingImage = QLabel(self)
        self.openingImage.setScaledContents(True)
        self.openingImage.setPixmap(QPixmap("resources/opening_image.png"))
        self.openingImage.setGeometry(0, 0, int(self.windowWidth * self.opening_power),
                                      int(self.windowHeight * self.opening_power))

        # [4]: Setting button to start a game
        self.playerNumber = None
        self.button: List[QPushButton] = []
        self.createSelectedPlayerButton()

    def GameSetup(self):
        # [1]: Setup Playboard & Background & Load Configuration + Gameplay

        self.background = QLabel(self)
        self.background.setPixmap(QPixmap("resources/map/background.png"))
        self.background.setGeometry(0, 0, self.max_width, self.max_height)
        self.background.show()

        self.GameLogic = GameLogic()
        self.move(0, 0)
        self.setFixedSize(self.max_width, self.max_height)

        self.playboard = QLabel(self)
        self.playboard.setPixmap(QPixmap("resources/map/compressed_playboard.png"))
        self.playboard.setGeometry(0, 0, self.max_height, self.max_height - 87)
        self.playboard.setScaledContents(True)
        self.playboard.show()

        # [2]: Add player into the game & Draw its information: Player Icon == LOL; Playing Icon: Lớp học mật ngữ
        non_repeated = []
        name = choice(PLAYER_NAME, size=4)
        icon = choice(PLAYER_ICON, size=4)
        self.playerLabel_List: List[List[QLabel]] = []

        for i in range(0, self.playerNumber):
            # Add Player
            non_repeated.append(name[i])
            non_repeated.append(icon[i])
            player = Player(ID="0xPlayer00" + str(i + 1), player_icon="resources/playerIcons/" + name[i] + IMG_FORMAT,
                            name=name[i], playing_icon='resources/playingIcons/' + icon[i] + IMG_FORMAT)
            player.setInitPosition(mapHeight=self.GameLogic.mapHeight)
            self.GameLogic.addPlayer(player_object=player)
            if i % 2 == 0:
                counter = 0
            else:
                counter = 1

            playerName = QLabel(self)
            playerName.setText(name[i])
            playerName.setScaledContents(True)
            playerName.setMouseTracking(True)
            playerName.setUpdatesEnabled(True)
            playerName.setFocus()
            playerName.setStyleSheet("color: red; font: bold; text-align: center")
            playerName.setGeometry(self.max_height + 200 + 400 * counter, 50 + 200 * (i // 2), 200, 50)
            playerName.show()

            playerIcon = QLabel(self)
            playerIcon.setScaledContents(True)
            playerIcon.setPixmap(QPixmap(player.player_icon))
            playerIcon.setUpdatesEnabled(True)
            playerIcon.setGeometry(self.max_height + 50 + 400 * counter, 50 + 200 * (i // 2), 120, 120)
            playerIcon.show()

            playerChest = QLabel(self)
            playerChest.setScaledContents(True)
            playerChest.setUpdatesEnabled(True)
            playerChest.setFocus()
            playerChest.setPixmap(QPixmap('resources/chest.png'))
            playerChest.setGeometry(self.max_height + 200 + 400 * counter, 110 + 200 * (i // 2), 70, 70)
            playerChest.show()

            player_num_chest = QLabel(self)
            player_num_chest.setText(": " + str(player.chest))
            player_num_chest.setUpdatesEnabled(True)
            player_num_chest.setScaledContents(True)
            player_num_chest.setMouseTracking(True)
            player_num_chest.setFocus()
            player_num_chest.setStyleSheet("color: white; font: bold")
            player_num_chest.setGeometry(self.max_height + 275 + 400 * counter, 110 + 200 * (i // 2), 200, 60)
            player_num_chest.show()

            self.playerLabel_List.append([playerName, playerIcon, playerChest, player_num_chest])

        # [3]: Draw Clock (QTimer + QLCDNumber to display) to measure the remaining time and Button to pass turn
        self.clock = QTimer()
        self.timing = self.DURATION
        self.clock.timeout.connect(self.update_timer)
        self.clock.start(self.CLOCK_UPDATE_SPEED)

        self.LCD_Clock = QLCDNumber(self)
        self.LCD_Clock.setDecMode()
        self.LCD_Clock.setDigitCount(6)
        self.LCD_Clock.setNumDigits(6)
        self.LCD_Clock.setMinimumHeight(200)
        self.LCD_Clock.setStyleSheet("color: red; border-style: outset")
        self.LCD_Clock.setSmallDecimalPoint(True)
        self.LCD_Clock.setGeometry(self.max_width - 250, self.max_height - 275, 225, 150)
        self.LCD_Clock.display(self.timing)
        self.LCD_Clock.show()

        self.passTurn_button = \
            CustomizedButton(self, iconPath='resources/passing_button_1.png',
                             hoveringIcon='resources/passing_button_2.png',
                             iconSize=[150, 150], position=[self.max_width - 350, self.max_height - 250])
        self.passTurn_button.pressed.connect(self.reset_clock)
        self.passTurn_button.show()

        # [4]: Draw all player image
        self.gamingIcon: List[QLabel] = []
        for player in self.GameLogic.playerList:

            player_gaming_icon = QLabel(self)
            player_gaming_icon.setPixmap(QPixmap(player.player_icon))

            player_gaming_icon.setGeometry(self.BASIC_POSITION[0] + player.x_position * self.COEF_DISTANCE_X,
                                           self.BASIC_POSITION[1] + player.y_position * self.COEF_DISTANCE_Y, 60, 60)
            player_gaming_icon.setScaledContents(True)
            player_gaming_icon.setUpdatesEnabled(True)
            player_gaming_icon.setMouseTracking(True)
            player_gaming_icon.setAutoFillBackground(False)
            player_gaming_icon.setFocus()
            player_gaming_icon.show()

            self.gamingIcon.append(player_gaming_icon)

        # [5]: Draw the dice to show the value of the dice
        # Dice[0]: Middle (1 rolled) --- Dice[1], Dice[2]: Lefty, Righty (2 rolled)
        self.visibleDice: List[QLabel] = []
        for i in range(0, 3):
            dice = QLabel(self)
            dice.setScaledContents(True)
            dice.setUpdatesEnabled(True)
            dice.setMouseTracking(True)
            dice.setEnabled(True)

            if i == 0:
                dice.setGeometry(self.max_height + 250, 450, 250, 250)
            else:
                dice.setGeometry(self.max_height + 50 + 400 * (i // 2), 450, 250, 250)
            dice.show()

            self.visibleDice.append(dice)

        # [6]: All the button that player can move and the chest's location
        self.spotList: List[CustomizedButton] = []      # Button List

        self.chestList: List[QLabel] = []               # Chest List
        self.__updateChestOnMap()

        self.number_of_turn = 1

        # [7]: Create timing
        self.fake_timing = self.DURATION
        self.dice: Union[List[int], int] = 0

        self.dice_clock = QTimer(self)
        self.dice_clock.timeout.connect(self.update_fakedice)
        self.dice_clock.start(self.DICE_ROLLING_SPEED)

        self.dice_clock_status: int = 1
        self.maximum_dice_can_rolled: int = 1

        # [8]: Run the game
        self.run_game()

    def makeFinalComment(self):
        # [1]: Reload the app
        self.setFixedSize(self.max_width, self.max_height)
        self.move(0, 0)
        self.update()
        self.show()

        # [2]: Finding all winner
        self.chestList: List[int] = [player.chest for player in self.GameLogic.playerList]
        self.chestList_idx = [i for i in range(0, len(self.chestList)) if self.chestList[i] == max(self.chestList)]

        self.current_idx: int = 0

        # [3]: Make GUI
        self.ending = CustomizedButton(self, iconPath='resources/ending_image.png',
                                       hoveringIcon='resources/ending_image.png',
                                       iconSize=[1920, 1002], position=[0, 0])
        self.ending.pressed.connect(self.showAllWinner)
        self.ending.show()

    # ------------------------------------------------------------------------------------------------
    # [1]: Used for predefined game
    def createSelectedPlayerButton(self):
        for i in range(0, 3):
            self.button.append(QPushButton(self))
            self.button[i].setGeometry(int(710 * self.opening_power), int(self.opening_power * (200 + 100*i)),
                                       int(141 * self.opening_power), int(51 * self.opening_power))
            self.button[i].pressed.connect(lambda i=i: self.setupPlayer(data=i+2))
            self.button[i].setText(str(i + 2) + " Players")
            self.button[i].show()

    def setupPlayer(self, data):
        if self.playerNumber is None:
            self.playerNumber = data

        self.GameSetup()

        self.openingImage.hide()
        for button in self.button:
            button.hide()

    # ------------------------------------------------------------------------------------------------
    # [2]: Running the game
    def update_timer(self):
        self.timing -= self.CLOCK_UPDATE_SPEED / 1000
        self.LCD_Clock.display(self.timing)
        if self.timing <= 0:
            self.reset_clock()

    def reset_clock(self):
        # Reset Clock (instant time)
        self.timing = self.DURATION
        self.fake_timing = self.DURATION
        self.LCD_Clock.display(self.timing)
        self.updateGameStatus()

    def reset_fake_clock(self):
        self.fake_timing = self.DURATION

    def run_game(self):
        self.maximum_dice_can_rolled = self.GameLogic.getNumDiceCanRolled()
        if self.maximum_dice_can_rolled == 1:
            self.visibleDice[0].show()
            self.visibleDice[1].hide()
            self.visibleDice[2].hide()

            self.dice = self.GameLogic.rollDice()

        else:
            self.visibleDice[0].hide()
            self.visibleDice[1].show()
            self.visibleDice[2].show()
            self.dice = [self.GameLogic.rollDice(), self.GameLogic.rollDice()]

        self.reset_fake_clock()

        self.update_movable_button()
        print("Turn #{} --------------------------------------------".format(self.number_of_turn))

    def update_fakedice(self):
        self.fake_timing -= self.DICE_ROLLING_SPEED / 1000
        # [1]: Showing the fake dice on the screen
        if self.maximum_dice_can_rolled == 1:
            if self.DURATION - self.fake_timing < self.DICE_STOPPING_TIME:
                # [1]: Showing the fake dice on the screen
                fake_dice = choice(DICE_IMAGE, size=1)

                self.visibleDice[0].setPixmap(QPixmap('resources/dice/' + fake_dice[0] + IMG_FORMAT))
                self.visibleDice[0].setScaledContents(True)
                self.visibleDice[0].update()
                self.visibleDice[0].repaint()
                # self.visibleDice[0].show()

            else:
                # [1]: Showing the real dice on the screen
                self.visibleDice[0].setPixmap(QPixmap('resources/dice/' + DICE_IMAGE[self.dice - 1] + IMG_FORMAT))
                self.visibleDice[0].setScaledContents(True)
                self.visibleDice[0].update()
                self.visibleDice[0].repaint()
                # self.visibleDice[0].show()

        elif self.maximum_dice_can_rolled == 2:
            if self.DURATION - self.fake_timing < self.DICE_STOPPING_TIME:
                fake_dice = choice(DICE_IMAGE, size=2)

                self.visibleDice[1].setPixmap(QPixmap('resources/dice/' + fake_dice[0] + IMG_FORMAT))
                self.visibleDice[1].setScaledContents(True)
                self.visibleDice[1].update()
                self.visibleDice[1].repaint()
                # self.visibleDice[1].show()

                self.visibleDice[2].setPixmap(QPixmap('resources/dice/' + fake_dice[1] + IMG_FORMAT))
                self.visibleDice[2].setScaledContents(True)
                self.visibleDice[2].update()
                self.visibleDice[2].repaint()
                # self.visibleDice[2].show()

            else:
                self.visibleDice[1].setPixmap(QPixmap('resources/dice/' + (DICE_IMAGE[self.dice[0] - 1]) + IMG_FORMAT))
                self.visibleDice[1].setScaledContents(True)
                self.visibleDice[1].update()
                self.visibleDice[1].repaint()
                # self.visibleDice[1].show()

                self.visibleDice[2].setPixmap(QPixmap('resources/dice/' + (DICE_IMAGE[self.dice[1] - 1]) + IMG_FORMAT))
                self.visibleDice[2].setScaledContents(True)
                self.visibleDice[2].update()
                self.visibleDice[2].repaint()
                # self.visibleDice[2].show()

        if self.fake_timing < 0:
            self.fake_timing = self.DURATION

    def update_movable_button(self):
        if self.maximum_dice_can_rolled == 1:
            all_path = self.GameLogic.find_path(dice=self.dice)
            for path in all_path:
                obj = CustomizedButton(self, iconPath='resources/playing_button_1.png',
                                       hoveringIcon='resources/playing_button_2.png',
                                       iconSize=[60, 60],
                                       position=[self.BASIC_POSITION[0] + path[0] * self.COEF_DISTANCE_X,
                                                 self.BASIC_POSITION[1] + path[1] * self.COEF_DISTANCE_Y])
                obj.pressed.connect(lambda path=path: self.move_the_player(x=path[0], y=path[1]))
                obj.show()
                self.spotList.append(obj)

        elif self.maximum_dice_can_rolled == 2:
            if 5 in self.dice or 6 in self.dice:
                self.move_the_player(x=11, y=6)
            else:
                pass

    def move_the_player(self, x, y):
        self.GameLogic.movePlayer(x=x, y=y)
        self.GameLogic.collectChestIfPossible()
        self.GameLogic.checkMapEvent()

        self.__updateChestOnMap()
        self.__updateGamingIcon(next_turn=False)
        self.__updatePlayerInformation(next_turn=False)
        self.__removeAllMovedButton()

    def updateGameStatus(self):
        if self.GameLogic.getRemainingMapChest() <= 0:
            self.makeFinalComment()
        else:
            # [1]: Update the game status
            self.GameLogic.move_to_new_turn()
            self.number_of_turn += 1

            if self.number_of_turn % self.playerNumber == 1 and self.number_of_turn != 1:
                self.GameLogic.destroyShop()

            # [2]: Update all the chest inside the shop on the map --- LOL Icon --- Gaming Icon
            self.__updateChestOnMap()
            self.__updatePlayerInformation(next_turn=True)
            self.__updateGamingIcon(next_turn=True)
            self.__removeAllMovedButton()

            # [3]: Looping one to create new turn
            self.run_game()

    def __updateChestOnMap(self):
        if self.chestList:
            for chest_image in self.chestList:
                chest_image.hide()
                chest_image.setEnabled(False)
            self.chestList.clear()

        for shop in self.GameLogic.StorageHouse:
            for chest_number in range(0, shop[2]):
                chest_image = QLabel(self)
                chest_image.setGeometry(self.BASIC_POSITION[0] + shop[1][0] * self.COEF_DISTANCE_X,
                                        self.BASIC_POSITION[1] + shop[1][1] * self.COEF_DISTANCE_Y,
                                        60, 60)
                chest_image.setPixmap(QPixmap('resources/chest.png'))
                chest_image.setScaledContents(True)
                chest_image.setUpdatesEnabled(True)
                chest_image.setMouseTracking(True)
                chest_image.show()
                self.chestList.append(chest_image)

    def __updatePlayerInformation(self, next_turn: bool = True):
        if next_turn is True:
            self.playerLabel_List.append(self.playerLabel_List[0])
            self.playerLabel_List.pop(0)

        for i in range(0, self.playerNumber):
            if i % 2 == 0:
                counter = 0
            else:
                counter = 1

            self.playerLabel_List[i][0].setGeometry(self.max_height + 200 + 400 * counter, 50 + 200 * (i // 2), 200, 50)
            self.playerLabel_List[i][0].update()
            self.playerLabel_List[i][0].show()

            self.playerLabel_List[i][1].setGeometry(self.max_height + 50 + 400 * counter, 50 + 200 * (i // 2), 120, 120)
            self.playerLabel_List[i][1].update()
            self.playerLabel_List[i][1].show()

            self.playerLabel_List[i][2].setGeometry(self.max_height + 200 + 400 * counter, 110 + 200 * (i // 2), 70, 70)
            self.playerLabel_List[i][2].update()
            self.playerLabel_List[i][2].show()

            self.playerLabel_List[i][3].setGeometry(self.max_height + 275 + 400 * counter, 110 + 200 * (i // 2), 200, 60)
            self.playerLabel_List[i][3].setText(": " + str(self.GameLogic.playerList[i].chest))
            self.playerLabel_List[i][3].update()
            self.playerLabel_List[i][3].show()

    def __updateGamingIcon(self, next_turn: bool = True):
        if next_turn is True:
            self.gamingIcon.append(self.gamingIcon[0])
            self.gamingIcon.pop(0)

        for i in range(0, self.playerNumber):
            tempPlayer = self.GameLogic.playerList[i]

            self.gamingIcon[i].setGeometry(self.BASIC_POSITION[0] + tempPlayer.x_position * self.COEF_DISTANCE_X,
                                           self.BASIC_POSITION[1] + tempPlayer.y_position * self.COEF_DISTANCE_Y,
                                           60, 60)
            self.gamingIcon[i].update()
            self.gamingIcon[i].show()

    def __removeAllMovedButton(self):
        if len(self.spotList) > 0:
            for button in self.spotList:

                button.hide()
                button.update()
            self.spotList.clear()

    # ------------------------------------------------------------------------------------------------
    # [3]: End the game
    def showAllWinner(self):
        self.ending.hide()

        large_image = QLabel(self)
        large_image.setPixmap(QPixmap('resources/ending_image_2.png'))
        large_image.setScaledContents(True)
        large_image.setGeometry(0, 0, 1920, 1080)

        icon = QLabel(self)
        icon.setPixmap(QPixmap(self.GameLogic.playerList[self.chestList_idx[0]].player_icon))
        icon.setGeometry(850, 440, 200, 200)
        icon.setScaledContents(True)

        info = QLabel(self)
        info.setText(str(self.GameLogic.playerList[self.chestList_idx[0]].name + ": " + str(max(self.chestList))))
        info.setScaledContents(True)
        info.setGeometry(850, 370, 200, 70)
        info.setStyleSheet("color: red; font: bold; text-align: center")

        large_image.show()
        icon.show()
        info.show()
