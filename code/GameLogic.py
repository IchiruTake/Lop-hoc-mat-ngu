import numpy as np
from player import Player
from typing import List
from numpy.random import choice, randint


class GameLogic:
    # [1]: Define Map
    MapGame = np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]], dtype=np.uint8)

    # [2]: Define Chest Location: ID - Storage Position - Chest Number - Access Position
    # Position: The first shows in x_position <-> The second show in y_position
    StorageHouse_NAME = ['Kính', 'Trái cây', 'Điện máy', 'Vải', 'Cá', 'Thịt', 'Kem', 'Gạo', 'Rau củ', 'Nước', 'Sốt',
                         'Giấy', 'Quặng', 'Bánh', 'Gỗ', 'Sơn', 'Keo', 'Gia vị', 'Board Game VN', 'Nhựa', 'Trường học',
                         'Siêu thị']
    StorageHouse = [['0xStore001', (10, 2), 2, (10, 0)], ['0xStore002', (6, 10), 1, (4, 10), (8, 10)],
                    ['0xStore003', (16, 14), 3, (16, 16)], ['0xStore004', (11, 14), 2, (14, 14)],
                    ['0xStore005', (2, 8), 1, (0, 8), (4, 8)], ['0xStore006', (2, 4), 1, (0, 4), (4, 4)],
                    ['0xStore007', (6, 4), 1, (8, 4)], ['0xStore008', (2, 2), 1, (2, 0), (0, 2)],
                    ['0xStore009', (2, 12), 1, (0, 12), (4, 12)], ['0xStore010', (6, 12), 1, (8, 12)],
                    ['0xStore011', (6, 14), 1, (6, 16)], ['0xStore012', (11, 4), 2, (14, 4)],
                    ['0xStore013', (12, 8), 2, (14, 8)], ['0xStore014', (6, 2), 1, (6, 0), (8, 2)],
                    ['0xStore015', (16, 11), 3, (14, 10)], ['0xStore016', (12, 2), 2, (14, 2)],
                    ['0xStore017', (16, 3), 3, (18, 4)], ['0xStore018', (2, 15), 1, (0, 14), (2, 16)],
                    ['0xStore019', (6, 7), 1, (8, 6)], ['0xStore020', (11, 12), 2, (14, 12)]]

    SpecialLocation = [['0xStore021', 'Trường học', 0, (11, 8)],
                       ['0xStore022', 'Siêu thị', 0, (18, 8)]]

    # [4]: Defined the initial Distance (main) that every standing blocks can possibly hold that person
    INIT_DISTANCE: int = 2

    def __init__(self):
        # [1]: Defined Map
        self.mapWidth = self.MapGame.shape[1]
        self.mapHeight = self.MapGame.shape[0]

        # [2]: Defined Player
        self.playerList: List[Player] = []
        self.playerTurnIdx = 0

        # [3]: Defined number of dice that the valid player can move
        self.num_dice_can_rolled = 1

    def getRemainingMapChest(self):
        chest = 0
        for shop in self.StorageHouse:
            chest += shop[2]
        return chest

    def addPlayer(self, player_object: Player):
        self.playerList.append(player_object)

    def setupPlayer(self, playerList: List[Player]):
        self.playerList = playerList

    def movePlayer(self, x: int, y: int):
        self.playerList[self.playerTurnIdx].setPosition(new_X=x, new_Y=y)

        player = self.playerList[self.playerTurnIdx]
        for other in self.playerList[self.playerTurnIdx + 1:]:
            if player.x_position == other.x_position and player.y_position == other.y_position:
                if other.chest > 0:
                    other.destroyChest()
                    player.receiveChest()

    def move_to_new_turn(self):
        """ This function is aims to create new turn for another players """
        self.playerList.append(self.playerList[0])
        self.playerList.pop(0)

    def rollDice(self):
        return np.random.randint(1, 7, size=1)[0]

    def getNumDiceCanRolled(self):
        """ If the player is at school, he/she can get 2 times of rolling a dice """
        if self.playerList[self.playerTurnIdx].x_position == self.SpecialLocation[0][3][0] and \
                self.playerList[self.playerTurnIdx].y_position == self.SpecialLocation[0][3][1]:
            self.num_dice_can_rolled = 2
        else:
            self.num_dice_can_rolled = 1
        return self.num_dice_can_rolled

    def checkMapValidity(self, current_Y, current_X):
        if self.MapGame[current_Y, current_X] == 1:
            return tuple([current_X, current_Y])
        elif self.MapGame[current_Y, current_X] == 0:
            if self.MapGame[current_Y, current_X - 1] == 1 and self.MapGame[current_Y, current_X + 1] == 1:
                pass
            elif self.MapGame[current_Y, current_X - 1] == 0 and self.MapGame[current_Y, current_X + 1] == 0:
                pass
            elif self.MapGame[current_Y, current_X - 1] == 0 and self.MapGame[current_Y, current_X + 1] == 1:
                return tuple([current_X + 1, current_Y])
            elif self.MapGame[current_Y, current_X - 1] == 1 and self.MapGame[current_Y, current_X + 1] == 0:
                return tuple([current_X - 1, current_Y])
        return None

    def find_path(self, dice: int):
        """ This function is aims to retrieve all of the position that player can move """
        valid_path = []

        """ This loop is used to find all valid positions on the map that the player can stand without anyone"""
        for i in range(0, dice + 1):
            HorizontalMove = i
            VerticalMove = dice - i

            # Checking the map on upper left: y(-); x(-)
            vertical_point = int(self.playerList[self.playerTurnIdx].y_position - VerticalMove * self.INIT_DISTANCE)
            horizontal_point = int(self.playerList[self.playerTurnIdx].x_position - HorizontalMove * self.INIT_DISTANCE)
            if vertical_point >= 0 and horizontal_point >= 0:
                path = self.checkMapValidity(current_Y=vertical_point, current_X=horizontal_point)
                if path is not None:
                    valid_path.append(path)

            # Checking the map on upper right: y(-); x(+)
            vertical_point = int(self.playerList[self.playerTurnIdx].y_position - VerticalMove * self.INIT_DISTANCE)
            horizontal_point = int(self.playerList[self.playerTurnIdx].x_position + HorizontalMove * self.INIT_DISTANCE)
            if vertical_point >= 0 and horizontal_point < self.mapWidth:
                path = self.checkMapValidity(current_Y=vertical_point, current_X=horizontal_point)
                if path is not None:
                    valid_path.append(path)

            # Checking the map on lower left: y(+), x(-)
            vertical_point = int(self.playerList[self.playerTurnIdx].y_position + VerticalMove * self.INIT_DISTANCE)
            horizontal_point = int(self.playerList[self.playerTurnIdx].x_position - HorizontalMove * self.INIT_DISTANCE)
            if vertical_point < self.mapHeight and horizontal_point >= 0:
                path = self.checkMapValidity(current_Y=vertical_point, current_X=horizontal_point)
                if path is not None:
                    valid_path.append(path)

            # Checking the map on lower right: y(+), x(+)
            vertical_point = int(self.playerList[self.playerTurnIdx].y_position + VerticalMove * self.INIT_DISTANCE)
            horizontal_point = int(self.playerList[self.playerTurnIdx].x_position + HorizontalMove * self.INIT_DISTANCE)
            if vertical_point < self.mapHeight and horizontal_point < self.mapWidth:
                path = self.checkMapValidity(current_Y=vertical_point, current_X=horizontal_point)
                if path is not None:
                    valid_path.append(path)

        temporary_validPath = list(set(valid_path))  # Remove all of the identical path (temporary)
        counter = [valid_path.count(spot) for spot in temporary_validPath]
        valid_path = list(set(valid_path))

        """ This variable is to get all of the position that other player stand in --> still valid position """
        stepOver = []
        for otherPlayer in self.playerList[self.playerTurnIdx + 1:]:
            for path in valid_path:
                if path[0] == otherPlayer.x_position and path[1] == otherPlayer.y_position:
                    stepOver.append(tuple([path[0], path[1]]))

        """ This variable shows all the index in the valid_path that if the player stands in the way of moving, 
        that path will not be considered to be valid (invalid_position)"""
        """
        invalid_path = []
        current_player = self.playerList[self.playerTurnIdx]
        for path in valid_path:
            # Getting the difference between the position and the player
            x_max = int(path[0] - current_player.x_position)
            y_max = int(path[1] - current_player.y_position)
            idx = valid_path.index(path)

            # Checking vertical path only --> No change in horizontal direction
            if x_max == 0:
                x_check = current_player.x_position
                for j in range(self.INIT_DISTANCE, abs(int(y_max)), self.INIT_DISTANCE):
                    # [1]: If the next position is at bottom (y_max > 0)
                    # [2]: If the next position is at top (y_max < 0)

                    if counter[idx] > 0:
                        if y_max < 0:
                            y_check = current_player.y_position - j
                        else:
                            y_check = current_player.y_position + j

                        # Refitting Data if the next point is over large
                        if y_check >= self.mapHeight:
                            y_check = self.mapHeight - 1
                        elif y_check < 0:
                            y_check = 0

                        validPosition = self.checkMapValidity(current_Y=y_check, current_X=x_check)
                        if validPosition is not None:
                            for other in self.playerList[self.playerTurnIdx + 1:]:
                                if other.x_position == validPosition[0] and other.y_position == validPosition[1]:
                                    invalid_path.append(path)
                                    counter[idx] -= 1
                        else:
                            counter[idx] -= 1
                    else:
                        break

            # Checking horizontal path only --> No change in vertical direction
            elif y_max == 0:
                y_check = current_player.y_position
                for j in range(self.INIT_DISTANCE, abs(int(x_max)), self.INIT_DISTANCE):
                    # [1]: If the next position is on the right (x_max > 0)
                    # [2]: If the next position is on the left (x_max < 0)
                    if counter[idx] > 0:
                        if x_max < 0:
                            x_check = current_player.x_position - j
                        else:
                            x_check = current_player.x_position + j

                        # Refitting Data if the next point is over large
                        if x_check >= self.mapWidth:
                            x_check = self.mapWidth - 1
                        elif x_check < 0:
                            x_check = 0

                        validPosition = self.checkMapValidity(current_Y=y_check, current_X=x_check)
                        if validPosition is not None:
                            for other in self.playerList[self.playerTurnIdx + 1:]:
                                if other.x_position == validPosition[0] and other.y_position == validPosition[1]:
                                    invalid_path.append(path)
                                    counter[idx] -= 1
                        else:
                            counter[idx] -= 1
                    else:
                        break

            # If there are both some changes in either two axis, we must check on two path:
            elif abs(x_max) != 0 and abs(y_max) != 0:
                # [1]: We must check on vertical axis first, then horizontal later
                # [2]: We must check on horizontal axis first, then vertical later
                # [3]: I will use if True: to have better separation before dealing with any number 

                if True:  # Case 1
                    for j in range(self.INIT_DISTANCE, abs(int(y_max)), self.INIT_DISTANCE):
                        # Keep the x_check is the x-axis point that the player is standing
                        if counter[idx] > 0:
                            x_check = current_player.x_position

                            if y_max < 0:
                                y_check = current_player.y_position - j
                            else:
                                y_check = current_player.y_position + j

                            if y_check >= self.mapHeight:
                                y_check = self.mapHeight - 1
                            elif y_check < 0:
                                y_check = 0

                            validPosition = self.checkMapValidity(current_Y=y_check, current_X=x_check)
                            if validPosition is not None:
                                for other in self.playerList[self.playerTurnIdx + 1:]:
                                    if other.x_position == validPosition[0] and other.y_position == validPosition[1]:
                                        invalid_path.append(path)
                                        counter[idx] -= 1
                            else:
                                counter[idx] -= 1
                        else:
                            break

                    for j in range(self.INIT_DISTANCE, abs(int(x_max)), self.INIT_DISTANCE):
                        # Keep the y_check is the y-axis point that next valid point
                        if counter[idx] > 0:
                            y_check = path[1]

                            if x_max < 0:
                                x_check = current_player.x_position - j
                            else:
                                x_check = current_player.x_position + j

                            if x_check >= self.mapWidth:
                                x_check = self.mapWidth - 1
                            elif x_check < 0:
                                x_check = 0

                            validPosition = self.checkMapValidity(current_Y=y_check, current_X=x_check)
                            if validPosition is not None:
                                for other in self.playerList[self.playerTurnIdx + 1:]:
                                    if other.x_position == validPosition[0] and other.y_position == validPosition[1]:
                                        invalid_path.append(path)
                                        counter[idx] -= 1
                            else:
                                counter[idx] -= 1

                        else:
                            break

                if True:  # Case 2
                    for j in range(self.INIT_DISTANCE, abs(int(x_max)), self.INIT_DISTANCE):
                        # Keep the y_check is the y-axis point that the player is standing
                        if counter[idx] > 0:
                            y_check = current_player.y_position

                            if x_max < 0:
                                x_check = current_player.x_position - j
                            else:
                                x_check = current_player.x_position + j

                            if x_check >= self.mapWidth:
                                x_check = self.mapWidth - 1
                            elif x_check < 0:
                                x_check = 0

                            validPosition = self.checkMapValidity(current_Y=y_check, current_X=x_check)
                            if validPosition is not None:
                                for other in self.playerList[self.playerTurnIdx + 1:]:
                                    if other.x_position == validPosition[0] and other.y_position == validPosition[1]:
                                        invalid_path.append(path)
                                        counter[idx] -= 1
                            else:
                                counter[idx] -= 1
                        else:
                            break

                    for j in range(self.INIT_DISTANCE, abs(int(y_max)), self.INIT_DISTANCE):
                        # Keep the y_check is the y-axis point that next valid point
                        if counter[idx] > 0:
                            x_check = path[0]

                            if y_max < 0:
                                y_check = current_player.y_position - j
                            else:
                                y_check = current_player.y_position + j

                            if y_check >= self.mapHeight:
                                y_check = self.mapHeight - 1
                            elif y_check < 0:
                                y_check = 0

                            validPosition = self.checkMapValidity(current_Y=y_check, current_X=x_check)
                            if validPosition is not None:
                                for other in self.playerList[self.playerTurnIdx + 1:]:
                                    if other.x_position == validPosition[0] and other.y_position == validPosition[1]:
                                        invalid_path.append(path)
                                        counter[idx] -= 1
                            else:
                                counter[idx] -= 1
                        else:
                            break
        """
        # Remove all identical index in the invalid_index and then re-create it
        # invalid_path = list(set(invalid_path))
        # temporary_validPath = [path for path in valid_path if path not in invalid_path]
        # valid_path = list(set(temporary_validPath + stepOver))
        FinalPath = list(set([valid_path[i] for i in range(0, len(valid_path)) if counter[i] > 0] + stepOver))
        return FinalPath

    def destroyShop(self):
        whichStorage = randint(0, len(self.StorageHouse), size=1)[0]
        while self.StorageHouse[whichStorage][2] == 0:
            whichStorage = randint(0, len(self.StorageHouse), size=1)[0]

        self.StorageHouse[whichStorage][2] = 0
        for player in self.playerList:
            for position in self.StorageHouse[whichStorage][3:]:
                if player.x_position == position[0] and player.y_position == position[1]:
                    player.destroyChest()

        return whichStorage

    def collectChestIfPossible(self):
        player = self.playerList[self.playerTurnIdx]
        for shop in self.StorageHouse:
            for valid_path in shop[3:]:
                if player.x_position == valid_path[0] and player.y_position == valid_path[1]:
                    player.receiveChest()
                    shop[2] -= 1
                    break

        if player.x_position == self.SpecialLocation[1][3][0] and player.y_position == self.SpecialLocation[1][3][1]:
            whichStorage = randint(0, len(self.StorageHouse), size=1)[0]
            while self.StorageHouse[whichStorage][2] == 0:
                whichStorage = randint(0, len(self.StorageHouse), size=1)[0]
            player.receiveChest()
            self.StorageHouse[whichStorage][2] -= 1

    def checkMapEvent(self):
        player = self.playerList[self.playerTurnIdx]

        ShopBoomingPosition = [(4, 16), (16, 0)]
        for position in ShopBoomingPosition:
            if player.x_position == position[0] and player.y_position == position[1]:
                self.destroyShop()
                player.destroyChest()
                break

        DrawEquipmentCardPosition = [(4, 14), (12, 16), (0, 6), (4, 2), (18, 0)]
        # for i in range(len(DrawEquipmentCardPosition)):
        #     self.drawEquipmentCard(equipmentDesk=equipmentDesk, numCardTaken=1)

        RemoveEquipmentCardPosition = [(12, 0), (18, 10)]
        # for i in range(len(RemoveEquipmentCardPosition)):
        #     if Position == RemoveEquipmentCardPosition[i]:
        #         PlayerDefault.checkImmunity()
        #         if self.immune is False:
        #             self.Equipment.pop(randint(0, len(self.Equipment) + 1, size=1)[0])

        RemoveChestPosition = [(18, 14)]
        for position in RemoveChestPosition:
            if player.x_position == position[0] and player.y_position == position[1]:
                player.destroyChest()
                break

        MoveThreeStep = [(8, 16)]
        for position in MoveThreeStep:
            if player.x_position == position[0] and player.y_position == position[1]:
                self.movePlayer(x=player.x_position + 3 * self.INIT_DISTANCE, y=player.y_position)
                break

        playerSkillRecovery = [(0, 10), (8, 14), (14, 6), (18, 12)]
        # for i in range(0, len(playerSkillRecovery)):
        #     if Position == playerSkillRecovery[i]:
        #         if self.skill1.activate is False:
        #             self.skill1.activate = True
        #         if self.skill2.activate is False:
        #             self.skill2.activate = True

        SchoolTeleport = [(4, 6), (8, 8), (10, 16), (2, 18)]
        # School Position: y = 8, x = 10
        for position in SchoolTeleport:
            if player.x_position == position[0] and player.y_position == position[1]:
                self.movePlayer(x=11, y=8)
                break
