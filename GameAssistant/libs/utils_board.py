# -*- coding: utf-8 -*-
from GameAssistant.gameboards.mafia import Mafia
from GameAssistant.gameboards.werewolf import Werewolf
from GameAssistant.gameboards.avalon import Avalon

def get_board_name_list():
    ret = []
    ret.append(Mafia.name)
    ret.append(Werewolf.name)
    ret.append(Avalon.name)
    return ret

def board_selector(boardname):
    if boardname in get_board_name_list():
            if boardname == 'Mafia':
                return Mafia
            elif boardname == 'Werewolf':
                return Werewolf
            elif boardname == 'Avalon':
                return Avalon
    raise Exception('Unknown board name!')

def board_factory(boardname, role_config={}):
    Board = board_selector(boardname)
    return Board(role_config)
