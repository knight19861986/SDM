# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.libs.utils_board import get_board_name_list
from GameAssistant.libs.utils_precheck import check_auth, check_game_state
from GameAssistant.libs.utils_board import get_board_name_list
from GameAssistant.libs.enums import GameState
from GameAssistant.gameboards.mafia import Mafia
from GameAssistant.gameboards.werewolf import Werewolf


@check_game_state(GameState.no.value, 'superuser')
def new(request, boardname, errorcode):
    messages = {
        '0': "Game code has already existed!",
        '1': "Illegal game code!",
        '2': "Num of players is not the same as the number of roles!"
    }
    if boardname not in get_board_name_list():
        url = reverse('GameAssistant:start_profile', args=[''])
        return HttpResponseRedirect(url)
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''
    return render(request, "initiate.html", {'board_name': boardname, 'error_msg': msg})


@check_auth('superuser')
def profile(request, errorcode):
    messages = {
        '0': "You have already started a game!\nPlease close the previous game before you start a new one!",
        '1': "You don't have an on-going game!\nPlease create a new one!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''
    return render(request, "profile.html", {'error_msg': msg})




