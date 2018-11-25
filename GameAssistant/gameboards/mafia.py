# -*- coding: utf-8 -*-
from GameAssistant.gameboards.boards import Role, Board

class Mafia(Board):
    name = 'Mafia'
    roles = [
        Role('Moderator','',1),
        Role('Mafia','',6),
        Role('Innocent','',6),
        Role('Detective','',6)
    ]

