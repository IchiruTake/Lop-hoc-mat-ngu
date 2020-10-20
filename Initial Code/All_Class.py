from numpy.random import shuffle, randint
import numpy as np
import os, sys, socket, socketserver
from time import time
import pandas as pd
from Default_Info import PlayerDefault, EquipmentDefault, StorageHouse, SpecialLocation, MapGame, mapLength, mapWidth


class Button:
    pass


class EquipmentCard(object):
    pass


class EquipmentDesk(object):
    max_EquipmentCard = 48

    def __init__(self, equipmentDesk: list[EquipmentCard] = []):
        if len(equipmentDesk) > self.max_EquipmentCard:
            return ValueError
        else:
            self.Equipment = equipmentDesk
            shuffle(self.Equipment)
            self.UsedCard = 0

    def countRemovedCard(self):
        for i in range(len(self.Equipment)):
            if self.Equipment[i].discard is True:
                self.UsedCard += 1

    def shuffleDesk(self):
        if len(self.Equipment) > 0:
            shuffle(self.Equipment)

    def recoverDesk(self):
        self.countRemovedCard()
        if self.UsedCard == self.max_EquipmentCard:
            for i in range(0, len(self.Equipment)):
                self.Equipment[i].discard = False
        self.UsedCard = 0


class SkillCard(object):
    pass


class Player(object):
    max_equipmentCard = 6
    max_playerSkill = 2

    def __init__(self, ID, equipment: list[EquipmentCard] = [], chest: int = 0):
        self.x_position = 0
        self.y_position = mapWidth - 1
        self.id = ID
        for i in range(len(PlayerDefault)):
            if self.id == PlayerDefault[i][0]:
                self.name = PlayerDefault[i][1]
                self.skill1 = None
                self.skill2 = None
        self.Equipment = equipment  # Equipment Card (objects) in list type
        self.chest = chest
        self.numRollDice = 1
        self.EquipmentDesk: list[EquipmentCard] = None
        self.overriddenPlayer: Player = None
        self.immune = False
        self.isMovable = True
        self.isMovableNextTurn = True
        self.movedAlready = False
        self.activateSkillCardAbility = True
        self.activateEquipmentCardAbility = True

    def compile(self, Desk: list[EquipmentCard]):
        self.EquipmentDesk = Desk

    def setDefaultEachTurn(self):
        self.immune = False
        self.isMovable = True
        self.movedAlready = False
        self.activateEquipmentCardAbility = True
        self.isMovableNextTurn = True
        self.overriddenPlayer = None

    def drawEquipmentCard(self, numCardTaken: int):
        for i in range(0, len(self.EquipmentDesk)):
            if self.EquipmentDesk[i].discard is False:
                if numCardTaken == 1:
                    TemporaryDesk = [self.EquipmentDesk[i]]
                elif numCardTaken > 1:
                    TemporaryDesk = self.EquipmentDesk[i: i + numCardTaken]
                    break
        self.Equipment += TemporaryDesk
        del TemporaryDesk
        self.checkEquipmentCard()

    def shuffleMyDesk(self):
        shuffle(self.Equipment)

    def checkEquipmentCard(self):
        while len(self.Equipment) > self.max_equipmentCard:
            self.Equipment.pop(randint(0, len(self.Equipment) + 1, size=1)[0])

    def collectChest(self):
        Position = (self.y_position, self.x_position)
        for i in range(0, len(StorageHouse)):
            for j in range(3, len(StorageHouse[i])):
                if Position == StorageHouse[i][j] and StorageHouse[i][2] > 0:
                    self.chest += 1
                    StorageHouse[i][2] -= 1

        if Position == SpecialLocation[1][3]:
            whichStorage = randint(0, len(StorageHouse), size=1)[0]
            while StorageHouse[whichStorage][2] == 0:
                whichStorage = randint(0, len(StorageHouse), size=1)[0]
            self.chest += 1
            StorageHouse[whichStorage][2] -= 1

    # ----------------------------------------------- set Movement -----------------------------------------------
    """ Finding location depends on the value of dice """
    def setPosition(self, X, Y):
        self.x_position = X
        self.y_position = Y

    def checkAtSchool(self):
        """ Check if they at school or not
            True: Player is currently at school
            False: Player has just graduated"""
        if self.x_position == 10 and self.y_position == 8:
            FirstDice = randint(1, 7, size=1)[0]
            SecondDice = randint(1, 7, size=1)[0]
            if FirstDice == 5 or FirstDice == 6 or SecondDice == 5 or SecondDice == 6:
                self.setPosition(X=11, Y=6)
                return False
            else:
                return True
        else:
            return False

    def checkImmunity(self):
        Answer = Player.selfProtectedFromMapEvent()
        if Answer is True:
            self.immune = True

    def checkMapEvent(self, equipmentDesk):
        """ This function is set after the player choose his/her location on the map.
            This function can track position and relating those position to identify which Map Event will be executed"""
        Position = (self.y_position, self.x_position)
        """ Check the map Event """
        ShopBoomingPosition = [(16, 4), (0, 16)]
        for i in range(0, len(ShopBoomingPosition)):
            if Position == ShopBoomingPosition[i]:
                Player.checkImmunity()
                if self.immune is False:
                    shopPosition = randint(0, len(StorageHouse), size=1)[0]
                    while StorageHouse[shopPosition][2] == 0:
                        shopPosition = randint(0, len(StorageHouse), size=1)[0]
                    StorageHouse[shopPosition][2] = 0

        DrawEquipmentCardPosition = [(14, 4), (16, 12), (6, 0), (2, 4), (0, 18)]
        for i in range(len(DrawEquipmentCardPosition)):
            self.drawEquipmentCard(equipmentDesk=equipmentDesk, numCardTaken=1)

        RemoveEquipmentCardPosition = [(0, 12), (10, 18)]
        for i in range(len(RemoveEquipmentCardPosition)):
            if Position == RemoveEquipmentCardPosition[i]:
                Player.checkImmunity()
                if self.immune is False:
                    self.Equipment.pop(randint(0, len(self.Equipment) + 1, size=1)[0])

        RemoveChestPosition = [(14, 18)]
        for i in range(len(RemoveChestPosition)):
            if Position == RemoveChestPosition[i]:
                Player.checkImmunity()
                if self.immune is False:
                    self.chest -= 1

        MoveThreeStep = [(16, 8)]
        for i in range(len(MoveThreeStep)):
            if Position == MoveThreeStep[i]:
                Player.checkImmunity()
                if self.immune is False:
                    self.setPosition(X=self.x_position + 3 * self.initDistance, Y=self.y_position)

        playerSkillRecovery = [(10, 0), (14, 8), (6, 14), (12, 18)]
        for i in range(0, len(playerSkillRecovery)):
            if Position == playerSkillRecovery[i]:
                if self.skill1.activate is False:
                    self.skill1.activate = True
                if self.skill2.activate is False:
                    self.skill2.activate = True

        SchoolTeleport = [(6, 4), (8, 8), (16, 10), (18, 2)]
        # School Position: y = 8, x = 10
        for i in range(len(SchoolTeleport)):
            Player.checkImmunity()
            if self.immune is False:
                if Position == SchoolTeleport[i]:
                    self.setPosition(X=10, Y=8)


class GameStatus(object):
    delayCardChosen = 5
    initDistance = 2

    def __init__(self, PlayerList: list[Player] = [], delay=45):
        self.delayEachTurn = delay
        self.chestRemaining = 32
        self.start_time = time()
        self.diceRolled = False
        self.clickPassTurn = False
        self.dataExchange = False
        self.endGame = False
        self.PlayerList = PlayerList
        self.turn = self.PlayerList[0].id
        if len(self.PlayerList) == 2:
            self.allPlayer = [self.PlayerList[1]]
        elif len(self.PlayerList) > 2:
            self.allPlayer = self.PlayerList[1:]
        self.dice = 0
        self.roundTurn: int = 0

    def getEquipmentCardBeginning(self):
        for i in range(0, len(self.PlayerList)):
            self.PlayerList[i].drawEquipmentCard(numCardTaken=3)

    def normalPrevention(self, opponentCard: EquipmentCard):
        delay = 3
        validNumber = ['005', '006', '007']
        Answer: type = bool  # if Yes = True: accept opponent can not use his card, else, pass
        for i in range(0, len(self.allPlayer)):
            for j in range(0, len(self.allPlayer[i].Equipment)):
                for num in validNumber:
                    if self.allPlayer[i].Equipment[j].id == '0xEquipCard' + num:
                        start = time()
                        while time() - start < delay:
                            print("Draw GUI at here")
                            print("Opponent use this card: ", opponentCard.name)
                            if Answer is True:
                                return Answer
        return False

    def checkRemainingChestForEndGame(self):
        self.chestRemaining = sum([int(StorageHouse[i]) for i in range(len(StorageHouse))])
        if self.chestRemaining == 0:
            self.endGame = True
            """ End Game Function"""
            print()

    def getRemainingTime(self):
        return round(self.delayEachTurn - (time() - self.start_time), 0)

    def setDelay(self, value):
        self.delayEachTurn = value

    def createEndTurnButton(self):
        """ Function here """
        pass

    def clickButtonForNextTurn(self):
        """ Click button function here"""
        self.clickPassTurn = True

    def resetTime(self):
        self.start_time = time()

    def setTurn(self):
        self.turn = self.PlayerList[0].id

    def switchPlayer(self):
        self.diceRolled = False
        self.dice = 0
        self.PlayerList[0].setDefaultEachTurn()
        self.PlayerList.append(self.PlayerList[0])
        self.PlayerList.pop(0)
        self.resetTime()

    def ShopExplosion(self):
        if type(self.roundTurn / len(self.PlayerList)) is int and self.roundTurn != 0:
            shopPosition = randint(0, len(StorageHouse), size=1)[0]
            while StorageHouse[shopPosition][2] == 0:
                shopPosition = randint(0, len(StorageHouse), size=1)[0]
            StorageHouse[shopPosition][2] = 0
            for player in self.PlayerList:
                Position = (player.y_position, player.x_position)
                for i in range(3, len(StorageHouse[shopPosition])):
                    if Position == StorageHouse[shopPosition][i]:
                        player.chest -= 1

    def moveToOtherTurn(self):
        if self.clickPassTurn is True or self.getRemainingTime() <= 0:
            if self.clickPassTurn is True:
                self.clickPassTurn = False
            """ Function here """
            self.roundTurn += 1
            self.ShopExplosion()
            self.switchPlayer()
            self.setTurn()

    def rollDice(self, dice: int = 0):
        self.diceRolled = True
        delay = 5
        if dice == 0:
            self.dice = randint(1, 7, size=1)[0]
            start = time()
            while time() - start < delay:
                tempDice = randint(1, 7, size=1)[0]
                tempDicePath = 'resources/dice/' + str(tempDice) + ' dot.png'
                """ Draw temporary Dice at here"""
            dicePath = 'resources/dice/' + str(self.dice) + ' dot.png'
            """ Remove temp Dice image and shows real dice. Show it for 'delay' time by real image """
            self.resetTime()
        else:
            pass

    @staticmethod
    def checkValidMap(Y, X):
        if MapGame[Y, X] == 1:
            validPosition = (Y, X)
        elif MapGame[Y, X] == 0:
            """ Prevent moving to unknown position """
            if MapGame[Y, X - 1] == 1 and MapGame[Y, X + 1] == 1:
                pass
            elif MapGame[Y, X - 1] == 0 and MapGame[Y, X + 1] == 0:
                pass
            elif MapGame[Y, X - 1] == 0 and MapGame[Y, X + 1] == 1:
                validPosition = (Y, X + 1)
            elif MapGame[Y, X - 1] == 1 and MapGame[Y, X + 1] == 0:
                validPosition = (Y, X - 1)
        return validPosition

    def findPath(self):
        validPath = []
        if self.PlayerList[0].checkAtSchool() is False:
            pass
        else:
            self.rollDice()
            for i in range(0, self.dice + 1):
                HorizontalMove = i
                VerticalMove = self.dice - HorizontalMove
                # Upper-Left Checking
                NewVerticalPosition = self.PlayerList[0].y_position - VerticalMove * self.initDistance
                NewHorizontalPosition = self.PlayerList[0].x_position - HorizontalMove * self.initDistance
                if NewVerticalPosition >= 0 and NewHorizontalPosition >= 0:
                    Upper_Left = self.checkValidMap(X=NewHorizontalPosition)
                    validPath.append(Upper_Left)

                # Upper-Right Checking
                NewVerticalPosition = self.PlayerList[0].y_position - VerticalMove * self.initDistance
                NewHorizontalPosition = self.PlayerList[0].x_position + HorizontalMove * self.initDistance
                if NewVerticalPosition >= 0 and NewHorizontalPosition < mapLength:
                    Upper_Right = self.checkValidMap(X=NewHorizontalPosition)
                    validPath.append(Upper_Right)

                # Bottom-Left Checking
                NewVerticalPosition = self.PlayerList[0].y_position + VerticalMove * self.initDistance
                NewHorizontalPosition = self.PlayerList[0].x_position - HorizontalMove * self.initDistance
                if NewVerticalPosition < mapWidth and NewHorizontalPosition >= 0:
                    Bottom_Left = self.checkValidMap(X=NewHorizontalPosition)
                    validPath.append(Bottom_Left)

                # Bottom-Right Checking
                NewVerticalPosition = self.PlayerList[0].y_position + VerticalMove * self.initDistance
                NewHorizontalPosition = self.PlayerList[0].x_position + HorizontalMove * self.initDistance
                if NewVerticalPosition < mapWidth and NewHorizontalPosition < mapLength:
                    Bottom_Right = self.checkValidMap(X=NewHorizontalPosition)
                    validPath.append(Bottom_Right)

            validPath = list(set(validPath))  # Remove identical position
            print('Initial Valid Path: ', validPath)
            # Check the map Validity if someone is on the 'location' (Valid)
            stepOver = [(validPath[j][0], validPath[j][1]) for i in range(0, len(self.allPlayer)) for j in
                        range(len(validPath))
                        if self.allPlayer[i].x_position == validPath[j][1] and self.allPlayer[i].y_position ==
                        validPath[j][0]]

            # Check the map Validity if someone is on the 'path' (Invalid)
            Temp = []
            for i in range(0, len(validPath)):
                y_max = validPath[i][0] - self.PlayerList[0].y_position
                x_max = validPath[i][1] - self.PlayerList[0].x_position
                # Vertical Only
                if x_max == 0:
                    x_check = self.PlayerList[0].x_position
                    for j in range(self.initDistance, abs(int(y_max)) + self.initDistance, self.initDistance):
                        if y_max < 0:
                            y_check = self.PlayerList[0].y_position - j
                        elif y_max >= 0:
                            y_check = self.PlayerList[0].y_position + j
                        if y_check >= mapWidth:
                            y_check = mapWidth - 1
                        elif y_check < 0:
                            y_check = 0
                        validPosition = self.checkValidMap(X=x_check)
                        for alpha in range(len(self.allPlayer)):
                            if self.allPlayer[alpha].x_position == validPosition[1] and \
                                    self.allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                # Horizontal Only
                elif y_max == 0:
                    y_check = self.PlayerList[0].y_position
                    for j in range(self.initDistance, abs(int(x_max)) + self.initDistance, self.initDistance):
                        if x_max < 0:
                            x_check = self.PlayerList[0].x_position - j
                        elif x_max >= 0:
                            x_check = self.PlayerList[0].x_position + j
                        if x_check >= mapLength:
                            x_check = mapLength - 1
                        elif x_check < 0:
                            x_check = 0
                        validPosition = self.checkValidMap(X=x_check)
                        for alpha in range(len(self.allPlayer)):
                            if self.allPlayer[alpha].x_position == validPosition[1] and \
                                    self.allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                elif abs(x_max) != 0 and abs(y_max) != 0:
                    """ Vertical (Keep x_check = self.x_position) -> Max ----> Horizontal -> Max """
                    for j in range(self.initDistance, abs(int(y_max)) + self.initDistance, self.initDistance):
                        x_check = self.PlayerList[0].x_position
                        if y_max < 0:
                            y_check = self.PlayerList[0].y_position - j
                        elif y_max >= 0:
                            y_check = self.PlayerList[0].y_position + j
                        if y_check >= mapWidth:
                            y_check = mapWidth - 1
                        elif y_check < 0:
                            y_check = 0
                        validPosition = self.checkValidMap(X=x_check)
                        for alpha in range(len(self.allPlayer)):
                            if self.allPlayer[alpha].x_position == validPosition[1] and \
                                    self.allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                    for j in range(self.initDistance, abs(int(x_max)) + self.initDistance, self.initDistance):
                        y_check = validPath[i][0]
                        if x_max < 0:
                            x_check = self.PlayerList[0].x_position - j
                        elif x_max >= 0:
                            x_check = self.PlayerList[0].x_position + j
                        if x_check >= mapLength:
                            x_check = mapLength - 1
                        elif x_check < 0:
                            x_check = 0
                        validPosition = self.checkValidMap(X=x_check)
                        for alpha in range(len(self.allPlayer)):
                            if self.allPlayer[alpha].x_position == validPosition[1] and \
                                    self.allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                    """ Horizontal (Keep y_check = self.y_position)-> Max ----> Vertical -> Max """
                    for j in range(self.initDistance, abs(int(x_max)) + self.initDistance, self.initDistance):
                        y_check = self.PlayerList[0].y_position
                        if x_max < 0:
                            x_check = self.PlayerList[0].x_position - j
                        elif x_max >= 0:
                            x_check = self.PlayerList[0].x_position + j
                        if x_check >= mapLength:
                            x_check = mapLength - 1
                        elif x_check < 0:
                            x_check = 0
                        validPosition = self.checkValidMap(X=x_check)
                        for alpha in range(len(self.allPlayer)):
                            if self.allPlayer[alpha].x_position == validPosition[1] and \
                                    self.allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                    for j in range(self.initDistance, abs(int(y_max)) + self.initDistance, self.initDistance):
                        x_check = validPath[i][1]
                        if y_max < 0:
                            y_check = self.PlayerList[0].y_position - j
                        elif y_max >= 0:
                            y_check = self.PlayerList[0].y_position + j
                        if y_check >= mapWidth:
                            y_check = mapWidth - 1
                        elif y_check < 0:
                            y_check = 0
                        validPosition = self.checkValidMap(X=x_check)
                        for alpha in range(len(self.allPlayer)):
                            if self.allPlayer[alpha].x_position == validPosition[1] and \
                                    self.allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

            # Merge the position
            Temp = list(set(Temp)).sort(reverse=True)
            for i in range(0, len(Temp)):
                validPath.pop(Temp[i])
            validPath = list(set(validPath + stepOver))
        return self.dice, validPath


# ---------------------------------------------------------------------------------------------------------------


class Player(Player):
    # ----------------------------------------------- Affected by Card -----------------------------------------------
    def selfProtectedFromOpponent(self, opponentCard: EquipmentCard):
        """ Draw a new board and Give that Player to choose their option to choose whether that card to be used to
            protect that Player against Opponent"""
        Answer: type = bool  # Yes = True: accept Protection; # No = False: decline Protection
        delay = 5
        validNumber = ['005', '006', '007', '012', '013']
        if self.activateEquipmentCardAbility is True:
            for i in range(0, len(self.Equipment)):
                for num in validNumber:
                    if self.Equipment[i].id == '0xEquipCard' + num:
                        start = time()
                        while time() - start <= delay:
                            print("Draw GUI at here with opponentCard shows here at the Player who are being attacked")
                            print("This is an opponentCard: ", opponentCard.name)
                            if Answer is True:
                                self.Equipment[i].deactivate()
                                self.Equipment[i].remove()
                                self.Equipment.pop(i)
                                return Answer
        return False

    def selfProtectedFromMapEvent(self):
        Answer: type = bool  # Yes = True: accept Protection; # No = False: decline Protection
        delay = 5
        validNumber = ['008', '009', '010', '011']
        if self.activateEquipmentCardAbility is True:
            for i in range(0, len(self.Equipment)):
                for num in validNumber:
                    if self.Equipment[i].id == '0xEquipCard' + num:
                        start = time()
                        while time() - start <= delay:
                            print("Draw GUI at here with opponentCard shows here at the Player who are being attacked")
                            if Answer is True:
                                self.Equipment[i].deactivate()
                                self.Equipment[i].remove()
                                self.Equipment.pop(i)
                                return Answer
        return False

    def setOverriddenPlayer(self, player: Player):
        self.overriddenPlayer = player


class EquipmentCard(EquipmentCard):
    def __init__(self, ID, owner: Player = None, target: Player = None, discard=False):
        self.id = ID
        for Info in EquipmentDefault:
            if self.id == Info[0]:
                self.name = Info[1]
                self.image = 'resources/Equipment/' + self.id + '.png'
        self.owner = owner  # This is the owner object
        self.target = target  # This is the target object
        self.discard = discard
        self.priority = 'min'

        self.GameStatus: GameStatus = None
        self.EquipmentDesk: EquipmentDesk = None
        self.allPlayer = None

    def remove(self):
        self.discard = True
        self.target = None

    def compile(self, Desk: EquipmentDesk, Status: GameStatus):
        self.GameStatus = Status
        self.EquipmentDesk = Desk
        if len(self.GameStatus.PlayerList) == 2:
            self.allPlayer = [self.GameStatus.PlayerList[1]]
        elif len(self.GameStatus.PlayerList) > 2:
            self.allPlayer = self.GameStatus.PlayerList[1:]

    def setTarget(self):
        """ Draw GUI related to how to set target """
        print()

    def activate(self):
        """ At the code line self.owner.Equipment.remove(self).
            The self can be changed when defining target """
        Sample = '0xEquipCard'
        # Đường Cấm (Not Done)
        if self.id == Sample + '001' or self.id == Sample + '002':
            if self.target.movedAlready is True:
                pass
            elif self.target.movedAlready is False and self.target.isMovable is True and self.owner.id != self.target.id:
                if self.target.x_position == 10 and self.target.y_position == 8:
                    pass
                else:
                    Answer: bool = self.target.selfProtectedFromOpponent(opponentCard=self)
                    self.owner.Equipment.remove(self)
                    self.remove()
                    if Answer is False:
                        self.target.isMovable = False
                        self.target.setOverridenPlayer(player=self.owner)
                        print("Writing GUI here to check whether the other player map to click on button.")

        # Siêu Đạo Chích
        if self.id == Sample + '003' or self.id == Sample + '004':
            if self.owner.id == self.GameStatus.turn and self.owner.id != self.target.id:
                Answer: bool = self.target.selfProtectedFromOpponent(opponentCard=self)
                self.owner.Equipment.remove(self)
                self.remove()
                if Answer is False:
                    x = randint(0, len(self.target.Equipment), size=1)[0]
                    self.owner.Equipment.append(self.target.Equipment[x])
                    self.target.Equipment.pop(x)

        # Quá Giang
        if self.id == Sample + '014' or self.id == Sample + '015':
            if self.target.x_position == 10 and self.target.y_position == 8 and self.owner.id != self.target.id:
                pass
            else:
                Answer: bool = self.target.selfProtectedFromOpponent(opponentCard=self)
                self.owner.Equipment.remove(self)
                self.deactivate()
                self.remove()
                if Answer is False:
                    opponentPosition = (self.target.y_position, self.target.x_position)
                    for i in range(0, len(StorageHouse)):
                        for j in range(3, len(StorageHouse[i])):
                            if opponentPosition == StorageHouse[i][j] and StorageHouse[i][2] >= 1:
                                self.owner.chest += 1
                                StorageHouse[i][2] -= 1

        # Lật Tẩy (Not Done)
        if self.id == Sample + '016' or self.id == Sample + '017':
            if self.owner.id == self.GameStatus.turn and self.owner.id != self.target.id:
                for i in range(0, len(self.allPlayer)):
                    Answer: bool = self.GameStatus.normalPrevention(opponentCard=self)
                    self.owner.Equipment.remove(self)
                    self.deactivate()
                    self.remove()
                    if Answer is False:
                        delay = 5
                        revealCard = EquipmentDesk.Equipment[0]
                        start = time()
                        while time() - start < delay:
                            """ Draw the revealCard at here """
                            print("This is the card: ", revealCard.name)

        # Bài Kiểm Tra A+
        if self.id == Sample + '018' or self.id == Sample + '019':
            if self.owner.id == self.GameStatus.turn:
                if self.owner.id == self.target.id:
                    self.owner.setPosition(X=11, Y=6)
                    self.owner.Equipment.remove(self)
                    self.remove()
                else:
                    if self.target.x_position == 10 and self.target.y_position == 8:
                        Answer: bool = self.target.selfProtectedFromOpponent(opponentCard=self)
                        if Answer is False:
                            self.target.setPosition(X=11, Y=6)
                            self.owner.Equipment.remove(self)
                            self.remove()

        # Đeo Bám (Not Done)
        if self.id == Sample + '020' or self.id == Sample + '021':
            if self.owner.id == self.GameStatus.turn:
                Answer: bool = self.target.selfProtectedFromOpponent(opponentCard=self)
                self.owner.Equipment.remove(self)
                self.deactivate()
                self.remove()
                if Answer is False:
                    validPath = [GameStatus.checkValidMap(X=self.target.x_position),
                                 GameStatus.checkValidMap(X=self.target.x_position),
                                 GameStatus.checkValidMap(X=self.target.x_position - self.GameStatus.initDistance),
                                 GameStatus.checkValidMap(X=self.target.x_position + self.GameStatus.initDistance)]
                    # Check your direction
                    for player in self.allPlayer:
                        PlayerPosition = (player.y_position, player.x_position)
                        i = 0
                        while i < len(validPath):
                            if PlayerPosition == validPath[i]:
                                validPath.pop(i)
                                break


class Button:
    image = 'resources/button/button.png'
    def __init__(self, y_position: int, x_position: int):
        self.y_position = y_position
        self.x_position = x_position
        self.click = False
        self.idClicker = None

    def getIdClicker(self):
        """ Function Here"""
        pass

    def clickButton(self, player: Player):
        """Check the mouse position"""
        mouse_X: type = int
        mouse_Y: type = int
        radius: type = int
        if player.overriddenPlayer is None:
            self.idClicker = player.id
            if mouse_X == self.x_position + radius and mouse_Y == self.y_position + radius:
                self.click = True
        else:
            self.idClicker = player.overriddenPlayer.id
            if mouse_X == self.x_position + radius and mouse_Y == self.y_position + radius:
                self.click = True

    def setMovement(self, player: Player):
        if self.click is True and self.idClicker == player.id:
            player.setPosition(X=self.x_position, Y=self.y_position)


class ButtonList(Button):
    def __init__(self, Path: list):
        self.AllButton: list[Button] = []
        for i in range(0, len(Path)):
            self.AllButton.append(Button(y_position=Path[i][0], x_position=Path[i][1]))

    def printInfo(self):
        for button in self.AllButton:
            print("The button is at (y, x) = ({}, {})".format(button.y_position, button.x_position))

    def setMovement(self, player: Player):
        for button in self.AllButton:
            if button.click is True:
                if player.overriddenPlayer is not None:
                    player.setPosition(X=button.x_position, Y=button.y_position)
                else:
                    player.isMovable = False



