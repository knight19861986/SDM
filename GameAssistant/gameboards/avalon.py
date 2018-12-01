# -*- coding: utf-8 -*-
from GameAssistant.gameboards.boards import Role, Board

class Avalon(Board):
    name = 'Avalon'
    roles = [       
        Role('Minions of Mordred','',6),
        Role('Arthurian Knights ','',6),
        Role('Merlin',''),
        Role('Percival',''),
        Role('Assassin',''),
        Role('Morgana',''),
        Role('Oberon',''),
        Role('Mordred','')
    ]

