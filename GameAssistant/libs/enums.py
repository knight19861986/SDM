# -*- coding: utf-8 -*-
from enum import Enum, unique

@unique
class SeatState(Enum):
    empty = 0
    superuser = 1
    subuser = 2

