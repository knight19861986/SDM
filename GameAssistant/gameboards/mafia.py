# -*- coding: utf-8 -*-
from GameAssistant.gameboards.boards import Role, Board

class Mafia(Board):
    name = 'Mafia'
    roles = [
        Role('Moderator','The game is run by a moderator, who does not participate as a real player'),
        Role('Mafia','The mafias pick a victim to kill every night.',6),
        Role('Innocent','',6),
        Role('Detective','',6)
    ]

