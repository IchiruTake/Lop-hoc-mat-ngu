from numpy.random import shuffle, randint
import numpy as np
import os, sys, socket, socketserver
from time import time
import pandas as pd

""" 
1) Order of ID versus Name is correct in order 
2) Thuật ngữ: In-turn: Dùng trong lượt của mình; Any-turn: Dùng lúc nào cũng được
Đặc biệt có loại dùng trước khi di chuyển, cấm dùng ở trường
"""

# -------------------------------------------- Default ID & Name Values --------------------------------------------
PlayerDefault = np.array(
    [['0xPC001', 'Thiên Bình', '0xPS001a', 'Ngoại giao khéo léo (Any-turn)', '0xPS001b', 'Nước hoa quyến rũ (In-turn)'],
     ['0xPC002', 'Xử Nữ', '0xPS002a', 'Trật tự (In-turn)', '0xPS002b', 'Quên đi (Any-turn)'],
     ['0xPC003', 'Cự Giải', '0xPS003a', 'Đồ ăn muôn năm (In-turn)', '0xPS003b', 'Năng khiếu bẩm sinh (In-turn)'],
     ['0xPC004', 'Kim Ngưu', '0xPS004a', 'Cho đi-nhận lại (In-turn)', '0xPS004b', 'Bỏ uổng vậy (Any-turn)'],
     ['0xPC005', 'Song Tử', '0xPS005a', 'Để tớ giúp cho (Any-turn)', '0xPS005b', 'Sao Chép (Any-turn)'],
     ['0xPC006', 'Nhân Mã', '0xPS006a', 'Ngựa quen đường cũ (In-turn)', '0xPS006b', 'Tốc biến (In-turn)'],
     ['0xPC007', 'Ma Kết', '0xPS007a', 'Tạo độ khó (Any-turn)', '0xPS007b', 'Điểm A+ siêu cấp (In-turn)'],
     ['0xPC008', 'Sư Tử', '0xPS008a', 'Năng lượng tích cực (Any-turn)', '0xPS008b', 'Chỉ đạo (Any-turn)'],
     ['0xPC009', 'Bạch Dương', '0xPS009a', 'Nhiệt tình (Any-turn)', '0xPS009b', 'Húc Văng (In-turn)'],
     ['0xPC010', 'Thiên Yết', '0xPS010a', 'Chơi công bằng (Any-turn)', '0xPS010b', 'Sao các cậu lạc quan quá vậy ('
                                                                                   'In-turn)'],
     ['0xPC011', 'Song Ngư', '0xPS011a', 'Thơm lây (Any-turn)', '0xPS011b', 'Âu Ơ ... Zzz (Any-turn)'],
     ['0xPC012', 'Bảo Bình', '0xPS012a', 'Đi ngược xu hướng (Any-turn)', '0xPS012b', 'Uống trà không (Any-turn)']])

StorageHouse = [['0xStore001', 'Kính', 2, (0, 10)],
                ['0xStore002', 'Trái cây', 1, (10, 4), (10, 8)],
                ['0xStore003', 'Điện máy', 3, (16, 16)],
                ['0xStore004', 'Vải', 2, (14, 14)],
                ['0xStore005', 'Cá', 1, (8, 0), (8, 4)],
                ['0xStore006', 'Thịt', 1, (4, 0), (4, 4)],
                ['0xStore007', 'Kem', 1, (4, 8)],
                ['0xStore008', 'Gạo', 1, (0, 2), (2, 0)],
                ['0xStore009', 'Rau củ', 1, (12, 0), (12, 4)],
                ['0xStore010', 'Nước', 1, (12, 8)],
                ['0xStore011', 'Sốt', 1, (16, 6)],
                ['0xStore012', 'Giấy', 2, (4, 14)],
                ['0xStore013', 'Quặng', 2, (8, 14)],
                ['0xStore014', 'Bánh', 1, (0, 6), (2, 8)],
                ['0xStore015', 'Gỗ', 3, (10, 14)],
                ['0xStore016', 'Sơn', 2, (2, 14)],
                ['0xStore017', 'Keo', 3, (4, 18)],
                ['0xStore018', 'Gia vị', 1, (14, 0), (16, 2)],
                ['0xStore019', 'Board Game VN', 1, (6, 8)],
                ['0xStore020', 'Nhựa', 2, (12, 14)]]
SpecialLocation = [['0xStore021', 'Trường học', 0, (8, 8)],
                   ['0xStore022', 'Siêu thị', 0, (8, 18)]]

EquipmentDefault = np.array([['0xEquipCard001', 'Đường cấm (Any-turn)'],
                             ['0xEquipCard002', 'Đường cấm (Any-turn)'],
                             ['0xEquipCard003', 'Siêu đạo chích (In-turn)'],
                             ['0xEquipCard004', 'Siêu đạo chích (In-turn)'],
                             ['0xEquipCard005', 'Sao cũng được (Any-turn)'],
                             ['0xEquipCard006', 'Sao cũng được (Any-turn)'],
                             ['0xEquipCard007', 'Sao cũng được (Any-turn)'],
                             ['0xEquipCard008', 'Trà lạc quan (Any-turn)'],
                             ['0xEquipCard009', 'Trà lạc quan (Any-turn)'],
                             ['0xEquipCard010', 'Trà lạc quan (Any-turn)'],
                             ['0xEquipCard011', 'Trà lạc quan (Any-turn)'],
                             ['0xEquipCard012', 'Ăn miếng trả miếng (Any-turn)'],
                             ['0xEquipCard013', 'Ăn miếng trả miếng (Any-turn)'],
                             ['0xEquipCard014', 'Quá giang (Any-turn)'],
                             ['0xEquipCard015', 'Quá giang (Any-turn)'],
                             ['0xEquipCard016', 'Lật tẩy (In-turn)'],
                             ['0xEquipCard017', 'Lật tẩy (In-turn)'],
                             ['0xEquipCard018', 'Bài kiểm tra A+ (In-turn)'],
                             ['0xEquipCard019', 'Bài kiểm tra A+ (In-turn)'],
                             ['0xEquipCard020', 'Đeo bám (In-turn)'],
                             ['0xEquipCard021', 'Đeo bám (In-turn)'],
                             ['0xEquipCard022', 'Tết thiếu nhi (In-turn)'],
                             ['0xEquipCard023', 'Tết thiếu nhi (In-turn)'],
                             ['0xEquipCard024', 'Vé xe bus (In-turn)'],
                             ['0xEquipCard025', 'Vé xe bus (In-turn)'],
                             ['0xEquipCard026', 'Giăng dây thừng (In-turn)'],
                             ['0xEquipCard027', 'Giăng dây thừng (In-turn)'],
                             ['0xEquipCard028', 'Lớp trưởng uy quyền (In-turn)'],
                             ['0xEquipCard029', 'Lớp trưởng uy quyền (In-turn)'],
                             ['0xEquipCard030', 'Quà sinh nhật (In-turn)'],
                             ['0xEquipCard031', 'Quà sinh nhật (In-turn)'],
                             ['0xEquipCard032', 'Dừng lại (Any-turn)'],
                             ['0xEquipCard033', 'Tới giờ học (Any-turn)'],
                             ['0xEquipCard034', 'Tranh hàng (Any-turn)'],
                             ['0xEquipCard035', 'Vé máy bay (In-turn)'],
                             ['0xEquipCard036', 'Cúp điện (Any-turn)'],
                             ['0xEquipCard037', 'Nước hoa thiên bình (In-turn)'],
                             ['0xEquipCard038', 'Nhà xí vẫy gọi (In-turn)'],
                             ['0xEquipCard039', 'Giày trượt patin (In-turn)'],
                             ['0xEquipCard040', 'Xí ngầu hoàn hảo (In-turn)'],
                             ['0xEquipCard041', 'Đôi bạn cùng tiến (Any-turn)'],
                             ['0xEquipCard042', 'Mua hàng Online (In-turn)'],
                             ['0xEquipCard033', 'Hack Xí ngầu -> 1'],
                             ['0xEquipCard044', 'Hack Xí ngầu -> 2'],
                             ['0xEquipCard045', 'Hack Xí ngầu -> 3'],
                             ['0xEquipCard046', 'Hack Xí ngầu -> 4'],
                             ['0xEquipCard047', 'Hack Xí ngầu -> 5'],
                             ['0xEquipCard048', 'Hack Xí ngầu -> 6']])
# ----------------------------------------------- Default Initiation -----------------------------------------------
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
                    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]], dtype=np.int8)
mapWidth = MapGame.shape[0]
mapLength = MapGame.shape[1]


class GameStatus(object):
    delayCardChosen = 5

    def __init__(self, start=time(), delay=45):
        self.delayEachTurn = delay
        self.chestRemaining = 32
        self.start_time = start
        self.diceRolled = False
        self.clickPassTurn = False
        self.dataExchange = False

    def checkRemainingChest(self):
        self.chestRemaining = sum([int(StorageHouse[i]) for i in range(len(StorageHouse))])
        if self.chestRemaining == 0:
            """ End Game """
            print()

    def getRemainingTime(self):
        return self.delayEachTurn - (time() - self.start_time)

    def setDelay(self, value):
        self.delayEachTurn = value

    def createEndTurnButton(self):
        """ Function here """
        pass

    def moveToOtherTurn(self):
        if self.clickPassTurn is True:
            self.clickPassTurn = False
            """ Function here """
            pass

    def rollDice(self):
        self.diceRolled = True
        delay = 5
        dice = randint(1, 7, size=1)[0]
        start_time = time()
        while time() - start_time < delay:
            """ Using GUI to make the dice random before assign the real value """

        dicePath = """ Reveal the dice according to the image path """
        return dice


class ExplosionDesk(object):
    def __init__(self, House=StorageHouse):
        self.Store = House
        self.ExplosionDesk = [self.Store[i][0] for i in range(len(self.Store))]
        shuffle(self.ExplosionDesk)
        self.UsedShopExplosionCard = []

    def drawExplosionCard(self):
        ExplosionCard = self.ExplosionDesk[0]
        self.ExplosionDesk = self.ExplosionDesk[1:]
        shuffle(self.ExplosionDesk)
        for i in range(len(self.Store)):
            if ExplosionCard == self.Store[i][0]:
                self.Store[i][2] == 0
        self.UsedShopExplosionCard.append(ExplosionCard)


class EquipmentDesk(object):
    max_EquipmentCard = 48

    def __init__(self, EquipmentDesk):
        self.Equipment = EquipmentDesk
        shuffle(self.Equipment)
        self.UsedDesk = []

    def shuffleDesk(self):
        if len(self.Equipment) > 0:
            shuffle(self.Equipment)
        if len(self.UsedDesk) > 0:
            shuffle(self.UsedDesk)

    def recoverDesk(self):
        if len(self.UsedDesk) == self.max_EquipmentCard:
            self.Equipment = self.UsedDesk
            for i in range(len(self.Equipment)):
                self.Equipment[i].discard = False


class Button(object):
    """Input the image path into here"""
    def __init__(self, y_position=None, x_position=None):
        self.y_position = y_position
        self.x_position = x_position
        self.click = False
        self.drawn = True

    def drawButton(self):
        """Writing draw button at here: Template: (y, x)"""
        pass

    def removeButton(self):
        """Writing delete button image: Template: (y, x)"""
        pass

    def clickButton(self):
        self.click = True

    def setMovement(self, player):
        if self.click is True:
            player.y_position = self.y_position
            player.x_position = self.x_position


class Player(object):
    max_equipmentCard = 6
    max_playerSkill = 2
    initDistance = 2

    class SkillCard:
        def __init__(self, ID, name, owner, activate=True, target=None):
            self.owner = owner
            self.target = target  # Opponent Object
            self.activate = activate
            self.priority = 'max'
            self.id = ID
            self.name = name
            self.image = None
            """Missing def activate SkillCard"""

        def selfProtected(self):
            print()

        def activateCard(self, whichTurn, allPlayer):
            Position = (self.owner.y_position, self.owner.x_position)
            if self.id == '0xPS001a' and self.activate is True:
                self.owner.drawEquipmentCard(equipmentDesk=self.target, numCardTaken=1)
            if self.id == '0xPS001b' and self.activate is True:
                if self.owner.turn == whichTurn:
                    if Position != SpecialLocation[0][3]:
                        self.target.beingAttacked(opponentCard=self)
                        validPath = []
                        if self.owner.y_position > 0:
                            Above = self.target.pathSelection(y_new=self.owner.y_position - self.owner.initDistance,
                                                              x_new=self.owner.x_position)
                            validPath.append(Above)
                        if self.owner.y_position < mapWidth:
                            Below = self.target.pathSelection(y_new=self.owner.y_position + self.owner.initDistance,
                                                              x_new=self.owner.x_position)
                            validPath.append(Below)
                        if self.owner.x_position > 0:
                            Left = self.target.pathSelection(y_new=self.owner.y_position,
                                                             x_new=self.owner.x_position - self.owner.initDistance)
                            validPath.append(Left)
                        if self.owner.x_position < mapLength:
                            Right = self.target.pathSelection(y_new=self.owner.y_position,
                                                              x_new=self.owner.x_position + self.owner.initDistance)
                            validPath.append(Right)

                        AllButton = []
                        for i in range(len(validPath)):
                            ButtonBlueprint = Button(y_position=validPath[i][0], x_position=validPath[i][1])
                            AllButton.append(ButtonBlueprint)
                        """ Needs function to click button """
                        for i in range(len(AllButton)):
                            AllButton[i].setMovement(player=self.target)
                    elif Position == SpecialLocation[0][3]:
                        self.target.setPosition(X=SpecialLocation[0][3][1], Y=SpecialLocation[0][3][0])

            if self.id == '0xPS002a' and self.activate is True:
                if self.owner.turn == whichTurn:
                    self.target.activateEquipmentCardAbility = False
                    self.target.beingAttacked(opponentCard=self)

            if self.id == '0xPS002b' and self.activate is True:
                if self.owner.isAttack is True:
                    self.target.activate = False

            if self.id == '0xPS003a' and self.activate is True:
                if self.owner.turn == whichTurn:
                    whichStorage = randint(0, len(StorageHouse), size=1)[0]
                    self.owner.chest = self.owner.chest + 1
                    StorageHouse[whichStorage][2] = StorageHouse[whichStorage][2] - 1

            if self.id == '0xPS003b' and self.activate is True:
                if self.owner.turn == whichTurn:
                    dice = randint(1, 7, size=1)[0]
                    """ Write the function that can choose the number of dice: 
                        Using GUI to select depends on images """

                    self.owner.findPath(allPlayer=allPlayer, Dice=dice)

    def __init__(self, ID, equipment=[], turn=None, chest=0):
        self.x_position = 0
        self.y_position = mapWidth - 1
        self.id = ID
        for i in range(len(PlayerDefault)):
            if self.id == PlayerDefault[i, 0]:
                self.name = PlayerDefault[i, 1]
                self.skill1 = self.SkillCard(ID=PlayerDefault[i, 2], name=PlayerDefault[i, 3], owner=self)
                self.skill2 = self.SkillCard(ID=PlayerDefault[i, 4], name=PlayerDefault[i, 5], owner=self)
        self.Equipment = equipment  # Equipment Card (objects) in list type

        self.turn = None  # ID_Player who can roll dice and move
        self.chest = chest
        self.numRollDice = 1

        self.immune = False
        self.isMovable = True
        self.isMovableNextTurn = True
        self.movedAlready = False
        self.activateSkillCardAbility = True
        self.activateEquipmentCardAbility = True
        self.isAttack = False
        self.attackingCard = None

    def beingAttacked(self, opponentCard):  # Counter-attack opponent
        self.isAttack = True
        self.attackingCard = opponentCard
        return opponentCard

    def setTurn(self, value):
        self.turn = value

    def setDefaultEachTurn(self):
        self.immune = False
        self.isMovable = True
        self.movedAlready = False
        self.activateEquipmentCardAbility = True
        self.isMovableNextTurn = True
        self.isAttack = False
        self.attackingCard = None

    def setPosition(self, X, Y):
        self.x_position = X
        self.y_position = Y

    """ Player get Equipment Cards """
    def shuffleDesk(self):
        shuffle(self.Equipment)

    def checkEquipmentCard(self):
        while len(self.Equipment) > self.max_equipmentCard:
            self.Equipment.pop(randint(0, len(self.Equipment) + 1, size=1)[0])
            if len(self.Equipment) <= self.max_equipmentCard:
                break

    def drawEquipmentCard(self, equipmentDesk, numCardTaken):
        if numCardTaken == 1:
            TemporaryDesk = equipmentDesk.Equipment[0]
            self.Equipment.append(TemporaryDesk)
        elif numCardTaken > 1:
            TemporaryDesk = equipmentDesk.Equipment[0: numCardTaken]
            for i in range(0, len(TemporaryDesk)):
                self.Equipment.append(TemporaryDesk[i])
        equipmentDesk.Equipment = equipmentDesk.Equipment[numCardTaken: len(equipmentDesk.Equipment)]
        equipmentDesk.shuffleDesk()
        self.checkEquipmentCard()

    def drawEquipmentCardBeginning(self, equipmentDesk):
        self.drawEquipmentCard(equipmentDesk=equipmentDesk, numCardTaken=3)

    """ Finding location depends on the value of dice """
    def pathSelection(self, y_new, x_new):
        if MapGame[y_new, x_new] == 1:
            validPosition = (y_new, x_new)
        elif MapGame[y_new, x_new] == 0:
            """ Prevent moving to unknown position """
            if MapGame[y_new, x_new - 1] == 1 and MapGame[y_new, x_new + 1] == 1:
                pass
            elif MapGame[y_new, x_new - 1] == 0 and MapGame[y_new, x_new + 1] == 0:
                pass
            elif MapGame[y_new, x_new - 1] == 0 and MapGame[y_new, x_new + 1] == 1:
                validPosition = (y_new, x_new + 1)
            elif MapGame[y_new, x_new - 1] == 1 and MapGame[y_new, x_new + 1] == 0:
                validPosition = (y_new, x_new - 1)
        return validPosition

    def checkAtSchool(self):
        """ Check if they at school or not
            True: Player is currently at school
            False: Player has just graduated"""
        if self.x_position == 10 and self.y_position == 8:
            dice_1 = randint(1, 7, size=1)[0]
            dice_2 = randint(1, 7, size=1)[0]
            if dice_1 == 5 or dice_1 == 6 or dice_2 == 5 or dice_2 == 6:
                self.setPosition(X=11, Y=8)
                return False
            else:
                return True
        elif self.x_position != 10 and self.y_position != 8:
            return False

    def findPath(self, allPlayer, Dice=None, schoolCheck=True):
        if schoolCheck is True:
            isAtSchool = self.checkAtSchool()
        if Dice is None:
            Dice = randint(1, 7, size=1)[0]
        else:
            pass
        if Dice > 0 and isAtSchool is False:
            validPath = []
            for i in range(0, Dice + 1):
                HorizontalMove = i
                VerticalMove = Dice - HorizontalMove
                # Upper-Left Checking
                NewVerticalPosition = self.y_position - VerticalMove * self.initDistance
                NewHorizontalPosition = self.x_position - HorizontalMove * self.initDistance
                if NewVerticalPosition >= 0 and NewHorizontalPosition >= 0:
                    Upper_Left = self.pathSelection(y_new=NewVerticalPosition, x_new=NewHorizontalPosition)
                    validPath.append(Upper_Left)

                # Upper-Right Checking
                NewVerticalPosition = self.y_position - VerticalMove * self.initDistance
                NewHorizontalPosition = self.x_position + HorizontalMove * self.initDistance
                if NewVerticalPosition >= 0 and NewHorizontalPosition < mapLength:
                    Upper_Right = self.pathSelection(y_new=NewVerticalPosition, x_new=NewHorizontalPosition)
                    validPath.append(Upper_Right)

                # Bottom-Left Checking
                NewVerticalPosition = self.y_position + VerticalMove * self.initDistance
                NewHorizontalPosition = self.x_position - HorizontalMove * self.initDistance
                if NewVerticalPosition < mapWidth and NewHorizontalPosition >= 0:
                    Bottom_Left = self.pathSelection(y_new=NewVerticalPosition, x_new=NewHorizontalPosition)
                    validPath.append(Bottom_Left)


                # Bottom-Right Checking
                NewVerticalPosition = self.y_position + VerticalMove * self.initDistance
                NewHorizontalPosition = self.x_position + HorizontalMove * self.initDistance
                if NewVerticalPosition < mapWidth and NewHorizontalPosition < mapLength:
                    Bottom_Right = self.pathSelection(y_new=NewVerticalPosition, x_new=NewHorizontalPosition)
                    validPath.append(Bottom_Right)

            validPath = list(set(validPath))  # Remove identical position
            print('Initial Valid Path: ', validPath)
            """ Check the map Validity if someone is on the 'location' (Valid) """
            stepOver = [(validPath[j][0], validPath[j][1]) for i in range(len(allPlayer)) for j in range(len(validPath))
                        if allPlayer[i].x_position == validPath[j][1] and allPlayer[i].y_position == validPath[j][0]]

            """ Check the map Validity if someone is on the 'path' (Invalid) """
            Temp = []
            for i in range(len(validPath)):
                y_max = validPath[i][0] - self.y_position
                x_max = validPath[i][1] - self.x_position
                # Vertical Only
                if x_max == 0:
                    x_check = self.x_position
                    for j in range(self.initDistance, abs(int(y_max)) + self.initDistance, self.initDistance):
                        if y_max < 0:
                            y_check = self.y_position - j
                        elif y_max >= 0:
                            y_check = self.y_position + j
                        if y_check >= mapWidth:
                            y_check = mapWidth - 1
                        elif y_check < 0:
                            y_check = 0
                        validPosition = self.pathSelection(y_new=y_check, x_new=x_check)
                        for alpha in range(len(allPlayer)):
                            if allPlayer[alpha].x_position == validPosition[1] and \
                                    allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                # Horizontal Only
                elif y_max == 0:
                    y_check = self.y_position
                    for j in range(self.initDistance, abs(int(x_max)) + self.initDistance, self.initDistance):
                        if x_max < 0:
                            x_check = self.x_position - j
                        elif x_max >= 0:
                            x_check = self.x_position + j
                        if x_check >= mapLength:
                            x_check = mapLength - 1
                        elif x_check < 0:
                            x_check = 0
                        validPosition = self.pathSelection(y_new=y_check, x_new=x_check)
                        for alpha in range(len(allPlayer)):
                            if allPlayer[alpha].x_position == validPosition[1] and \
                                    allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                elif abs(x_max) != 0 and abs(y_max) != 0:
                    """ Vertical (Keep x_check = self.x_position) -> Max ----> Horizontal -> Max """
                    for j in range(self.initDistance, abs(int(y_max)) + self.initDistance, self.initDistance):
                        x_check = self.x_position
                        if y_max < 0:
                            y_check = self.y_position - j
                        elif y_max >= 0:
                            y_check = self.y_position + j
                        if y_check >= mapWidth:
                            y_check = mapWidth - 1
                        elif y_check < 0:
                            y_check = 0
                        validPosition = self.pathSelection(y_new=y_check, x_new=x_check)
                        for alpha in range(len(allPlayer)):
                            if allPlayer[alpha].x_position == validPosition[1] and \
                                    allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                    for j in range(self.initDistance, abs(int(x_max)) + self.initDistance, self.initDistance):
                        y_check = validPath[i][0]
                        if x_max < 0:
                            x_check = self.x_position - j
                        elif x_max >= 0:
                            x_check = self.x_position + j
                        if x_check >= mapLength:
                            x_check = mapLength - 1
                        elif x_check < 0:
                            x_check = 0
                        validPosition = self.pathSelection(y_new=y_check, x_new=x_check)
                        for alpha in range(len(allPlayer)):
                            if allPlayer[alpha].x_position == validPosition[1] and \
                                    allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                    """ Horizontal (Keep y_check = self.y_position)-> Max ----> Vertical -> Max """
                    for j in range(self.initDistance, abs(int(x_max)) + self.initDistance, self.initDistance):
                        y_check = self.y_position
                        if x_max < 0:
                            x_check = self.x_position - j
                        elif x_max >= 0:
                            x_check = self.x_position + j
                        if x_check >= mapLength:
                            x_check = mapLength - 1
                        elif x_check < 0:
                            x_check = 0
                        validPosition = self.pathSelection(y_new=y_check, x_new=x_check)
                        for alpha in range(len(allPlayer)):
                            if allPlayer[alpha].x_position == validPosition[1] and \
                                    allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

                    for j in range(self.initDistance, abs(int(y_max)) + self.initDistance, self.initDistance):
                        x_check = validPath[i][1]
                        if y_max < 0:
                            y_check = self.y_position - j
                        elif y_max >= 0:
                            y_check = self.y_position + j
                        if y_check >= mapWidth:
                            y_check = mapWidth - 1
                        elif y_check < 0:
                            y_check = 0
                        validPosition = self.pathSelection(y_new=y_check, x_new=x_check)
                        for alpha in range(len(allPlayer)):
                            if allPlayer[alpha].x_position == validPosition[1] and \
                                    allPlayer[alpha].y_position == validPosition[0]:
                                Temp.append(i)

            """ Merge the position """
            Temp = list(set(Temp))
            Temp.sort(reverse=True)
            print('Overlaped Position: ', Temp)
            for i in range(0, len(Temp)):
                validPath.pop(Temp[i])
            validPath = list(set(validPath + stepOver))
        elif Dice == 0:
            pass
        return Dice, validPath

    """ Setup Map Event """
    def checkMapEvent(self, ExplosionDesk, equipmentDesk):
        """ This function is set after the player choose his/her location on the map.
            This function can track position and relating those position to identify which Map Event will be executed"""
        Position = (self.y_position, self.x_position)

        """ Check the map Event """
        ShopBoomingPosition = [(16, 4), (0, 16)]
        for i in range(len(ShopBoomingPosition)):
            if Position == ShopBoomingPosition[i]:
                ExplosionDesk.drawExplosionCard()

        DrawEquipmentCardPosition = [(14, 4), (16, 12), (6, 0), (2, 4), (0, 18)]
        for i in range(len(DrawEquipmentCardPosition)):
            if Position == DrawEquipmentCardPosition[i]:
                self.drawEquipmentCard(equipmentDesk=equipmentDesk, numCardTaken=1)

        RemoveEquipmentCardPosition = [(0, 12), (10, 18)]
        for i in range(len(RemoveEquipmentCardPosition)):
            if Position == RemoveEquipmentCardPosition[i]:
                self.Equipment.pop(randint(0, len(self.Equipment) + 1, size=1)[0])

        RemoveChestPosition = [(14, 18)]
        for i in range(len(RemoveChestPosition)):
            if Position == RemoveChestPosition[i]:
                self.chest = self.chest - 1
                ExplosionDesk.chestExplosion = ExplosionDesk.chestExplosion + 1

        MoveThreeStep = [(16, 8)]
        for i in range(len(MoveThreeStep)):
            if Position == MoveThreeStep[i]:
                self.x_position = self.x_position + 3 * self.initDistance
                self.y_position = self.y_position

        playerSkillRecovery = [(10, 0), (14, 8), (6, 14), (12, 18)]
        for i in range(0, len(playerSkillRecovery)):
            if self.skill1.activate is False:
                self.skill1.activate = True
            if self.skill2.activate is False:
                self.skill2.activate = True

        SchoolTeleport = [(6, 4), (8, 8), (16, 10), (18, 2)]
        # School Position: y = 8, x = 10
        for i in range(len(SchoolTeleport)):
            if Position == SchoolTeleport[i]:
                self.x_position = 10
                self.y_position = 8

        """ Collect Chest if the Player's Position is fulfilled """
        for i in range(len(StorageHouse)):
            for j in range(3, len(StorageHouse[i])):
                if Position == StorageHouse[i][j] and StorageHouse[i][2] > 0:
                    self.chest = self.chest + 1
                    StorageHouse[i][2] = StorageHouse[i][2] - 1
        if Position == StorageHouse[1][3]:
            whichStorage = randint(0, len(StorageHouse), size=1)[0]
            if StorageHouse[whichStorage][2] >= 1:
                self.chest = self.chest + 1
                StorageHouse[whichStorage][2] = StorageHouse[whichStorage][2] - 1
            else:
                pass


class EquipmentCard(object):
    def __init__(self, ID, name, image, owner=None, activate=True, target=None, discard=False):
        self.id = ID
        self.name = name
        self.image = image
        self.owner = owner  # This is the owner object
        self.target = target  # This is
        self.discard = discard
        self.activate = activate
        self.priority = 'min'

    def remove(self, equipmentDesk):
        self.discard = True
        equipmentDesk.UsedDesk.append(self)

    def checkImmunity(self):
        for i in range(len(self.target.Equipment)):
            if self.target.Equipment.id == '0xEquipCard005' or self.target.Equipment.id == '0xEquipCard006' or \
                    self.target.Equipment.id == '0xEquipCard007':
                self.target.immune = True
            else:
                pass

    def selfProtected(self, opponentCard):
        if self.owner.activateEquipmentCardAbility is True:
            if self.id == '0xEquipCard008' or self.id == '0xEquipCard009' or \
                    self.id == '0xEquipCard010' or self.id == self.id == '0xEquipCard011':
                self.owner.immune = True  # One-turn Only
            if self.id == '0xEquipCard012' or self.id == '0xEquipCard013':
                if self.owner.isAttack is True:
                    opponentCard.activateCard(self, player=self.target, opponent=self.owner)


    def activateCard(self, whichTurn, allPlayer, equipmentDesk, dice=None):
        """ Make the card function"""
        if self.owner.activateEquipmentCardAbility is True:
            if self.id == '0xEquipCard001' or self.id == '0xEquipCard002':
                if self.target.id != self.owner.id:
                    if self.target.x_position == 10 and self.target.y_position == 9:
                        """ Invalid function """
                    else:
                        self.checkImmunity()
                        if self.target.immune is True:
                            pass
                        else:
                            self.target.isMovable = False
                            self.target.beingAttacked(opponentCard=self)
                            self.target.findPath(allPlayer=allPlayer)
                            """"""

                            self.remove(equipmentDesk=equipmentDesk)
                        """"""
                else:
                    pass
            if self.id == '0xEquipCard003' or self.id == '0xEquipCard004':
                if self.owner.turn == whichTurn:
                    self.checkImmunity()
                    if self.target.immune is True:
                        pass
                    else:
                        self.target.beingAttacked(opponentCard=self)
                        self.owner.drawEquipmentCard(equipmentDesk=self.target, numCardTaken=1)

                        self.remove(equipmentDesk=equipmentDesk)
                else:
                    """ Invalid function """

            if self.id == '0xEquipCard014' or self.id == '0xEquipCard015':
                for i in range(0, len(StorageHouse)):
                    for j in range(3, len(StorageHouse[i])):
                        if self.target.x_position == StorageHouse[i][j][1] and \
                                self.target.y_position == StorageHouse[i][j][0] and StorageHouse[i][2] > 0:
                            self.owner.chest = self.owner.chest + 1
                            StorageHouse[i][2] = StorageHouse[i][2]

                self.remove(equipmentDesk=equipmentDesk)

            if self.id == '0xEquipCard016' or self.id == '0xEquipCard017':
                if self.owner.id == whichTurn:
                    revealCard = equipmentDesk.Equipment[0]
                    """ Showing the card identity at here """
                    self.remove(equipmentDesk=equipmentDesk)

            if self.id == '0xEquipCard018' or self.id == '0xEquipCard019':
                if self.owner.id == whichTurn:
                    self.target.x_position = 11
                    self.target.y_position = 6



# ----------------------------------------------------------------------------------------------
def ExportData(playerList):
    Columns = ['Status', 'Player 1', 'Player 2', 'Player 3', 'Player 4']
    Database = [["Player's ID", playerList[0].id, playerList[1].id, playerList[2].id, playerList[3].id],
                ["Player's Name", playerList[0].name, playerList[1].name, playerList[2].name, playerList[3].name],
                ["Y", playerList[0].y_position, playerList[1].y_position, playerList[2].y_position, playerList[3].y_position],
                ["X", playerList[0].x_position, playerList[1].x_position, playerList[2].x_position, playerList[3].x_position],
                ['Player Turn', playerList[0].turn, playerList[1].turn, playerList[2].turn, playerList[3].turn]]
    GeneralData = pd.DataFrame(data=Database, index=None, columns=Columns)
    GeneralData.to_csv(path_or_buf='exchangeData\InfoData.csv', index=False)


Player1 = Player(ID=PlayerDefault[0, 0], equipment=None)
Player1.setPosition(X=6, Y=8)
Player2 = Player(ID=PlayerDefault[1, 0], equipment=None)
Player2.setPosition(X=8, Y=8)
Player3 = Player(ID=PlayerDefault[2, 0], equipment=None)
Player3.setPosition(X=11, Y=6)
Player4 = Player(ID=PlayerDefault[3, 0], equipment=None)
Player4.setPosition(X=10, Y=8)
playerTurn = [Player1, Player2, Player3, Player4]
for i in range(0, len(playerTurn)):
    playerTurn[i].setTurn(value=playerTurn[0].id)

Status = GameStatus(start=time(), delay=1)
while Status.chestRemaining >= 0:
    if Status.getRemainingTime() > 0:
        if Status.dataExchange is False:
            ExportData(playerList=playerTurn)
            Status.dataExchange = True
        # print(Status.chestRemaining)
        # print('Remaining Time = {:.2f} s'.format(Status.getRemainingTime()))
        if playerTurn[0].isMovable is True and Status.diceRolled is False:
            dice, ValidPath = playerTurn[0].findPath(allPlayer=playerTurn[1:len(playerTurn)])
            print('Player: {} --- Dice: {} --> ValidPath: {}'.format(playerTurn[0].name, dice, ValidPath))
            print("-----------------------")
            Status.diceRolled = True
        buttonObject = [Button(y_position=ValidPath[i][0], x_position=ValidPath[i][0]) for i in range(len(ValidPath))]
        for i in range(len(buttonObject)):
            buttonObject[i].drawButton()
            """ Other Code """
            if buttonObject[i].click is True:
                buttonObject[i].setMovement(player=playerTurn[0])
                playerTurn[0].movedAlready = True
            buttonObject[i].removeButton()
    elif Status.getRemainingTime() <= 0 or Status.clickPassTurn is True:
        Status.checkRemainingChest()
        Status = GameStatus(start=time(), delay=1)

        playerTurn[0].setDefaultEachTurn()
        playerTurn.append(playerTurn[0])
        """ Add code related to object' attribute """
        playerTurn.pop(0)
        for i in range(0, len(playerTurn)):
            playerTurn[i].setTurn(value=playerTurn[0].id)

