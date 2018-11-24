# -*- coding: utf-8 -*-
from enum import Enum, unique

@unique
class SeatState(Enum):
    empty = 0
    superuser = 1
    subuser = 2


@unique
class GameState(Enum):
    no = 0
    preparing = 1
    started = 2
    ended = 4


@unique
class RefreshType(Enum):
    nothing = 0
    username = 1
    seat = 2
    other_01 = 4 #For future scalability
    other_02 = 8 #For future scalability

