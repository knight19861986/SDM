# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest, JsonResponse
from GameAssistant.gameboards.mafia import Mafia
from GameAssistant.gameboards.werewolf import Werewolf
from GameAssistant.libs.utils_precheck import check_auth
from GameAssistant.libs.utils_board import get_board_name_list, board_selector

@check_auth('superuser')
def get_board_list(request):
    try:
        ret = get_board_name_list()
        return JsonResponse(ret, safe=False)
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_board_list! Details: {0}'.format(e))

@check_auth('user')
def get_board_roles(request, boardname):
    try:
        ret = []
        Board = board_selector(boardname)
        for role in Board.roles:
            ret.append({
                'RoleName': role.name,
                'Description': role.description,
                'Maximum': role.maximum,
                })
        return JsonResponse(ret, safe=False)

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_board_roles! Details: {0}'.format(e))
