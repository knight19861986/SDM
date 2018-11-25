# -*- coding: utf-8 -*-
from GameAssistant.gameboards.mafia import Mafia
from GameAssistant.gameboards.werewolf import Werewolf
# from GameAssistant.gameboards.avalon import Avalon

def get_board_name_list():
    ret = []
    ret.append(Mafia.name)
    ret.append(Werewolf.name)
    # ret.append(Avalon.name)
    ret.append("Avalon")
    return ret