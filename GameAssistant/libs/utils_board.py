# -*- coding: utf-8 -*-
from GameAssistant.gameboards.mafia import Mafia
from GameAssistant.gameboards.werewolf import Werewolf

def get_board_name_list():
    ret = []
    ret.append(Mafia.name)
    ret.append(Werewolf.name)
    return ret