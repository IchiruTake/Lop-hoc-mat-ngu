
class Player:
    def __init__(self, ID: str, player_icon: str, name: str, playing_icon: str):
        # [1]: Definition
        self.id = ID
        self.player_icon = player_icon
        self.name = name
        self.playing_icon = playing_icon

        # [2]: Possessing
        self.chest = 0

        # [3]: Current Status (boolean)
        self.resistance: int = 2
        self.immune = False
        self.isMovable = True
        self.isMovableNextTurn = True
        self.movedAlready = False

        # [4]: Player's Position:
        self.x_position = 0
        self.y_position = 0

    def getPlayerID(self):
        return self.id

    def setName(self, name):
        self.name = name

    def regainStatus(self):
        self.immune = False
        self.isMovable = True
        self.isMovableNextTurn = True
        self.movedAlready = False

    def setPosition(self, new_X, new_Y):
        self.x_position = new_X
        self.y_position = new_Y

    def setInitPosition(self, mapHeight: int):
        self.x_position = 0
        self.y_position = mapHeight - 1

    def getPosition(self):
        return tuple([self.x_position, self.y_position])

    def receiveChest(self):
        self.chest += 1

    def destroyChest(self):
        self.chest -= 1