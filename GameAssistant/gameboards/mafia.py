# -*- coding: utf-8 -*-
from board import Role, Board

class Mafia(Board):
    name = 'Mafia'
    roles = [
        Role('Moderator',''),
        Role('Mafia',''),
        Role('Innocent',''),
        Role('Detective','')
    ]

