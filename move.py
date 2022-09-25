from typing import Tuple, Optional

class Move(object):
    def __init__(self, from_position : Tuple[int, int], to_position : Tuple[int, int], attack_position : Tuple[int, int], id : Optional[int] = -1):
        self.__x0, self.__y0 = from_position
        self.__x1, self.__y1 = to_position
        self.__ax, self.__ay = attack_position
        self.__player_id = id # While optional (since the player could generate the move) it does need to be set for it to be a valid move

    #<editor-fold> Properties
    @property
    def x0(self):
        return self.__x0

    @property
    def y0(self):
        return self.__y0

    @property
    def ax(self):
        return self.__ax

    @property
    def ay(self):
        return self.__ay

    @property
    def x1(self):
        return self.__x1

    @property
    def y1(self):
        return self.__y1

    @property
    def start(self):
        return self.x0, self.y0

    @property
    def end(self):
        return self.x1, self.y1

    @property
    def attack(self):
        return self.ax, self.ay

    @property
    def id(self):
        return self.__player_id

    @id.setter
    def id(self, id : int) -> None:
        self.__player_id = id

    #</editor-fold> Properties

    def __str__(self):
        return f"{self.id}: {self.x0, self.y0} -> {self.x1, self.y1} @ {self.ax, self.ay}"

    def __repr__(self):
        return f"{self.id=}, {self.x0=}, {self.y0=}, {self.x1=}, {self.y1=}, {self.ax=}, {self.ay=}"
