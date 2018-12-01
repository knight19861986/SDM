# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.games import Game
from GameAssistant.libs.utils_precheck import check_game_state
from GameAssistant.libs.enums import GameState

@check_game_state(GameState.preparing.value+GameState.started.value+GameState.ended.value, 'superuser')
def room(request):
    return render(request, "room_superuser.html")


@check_game_state(GameState.preparing.value+GameState.started.value+GameState.ended.value, 'subuser')
def room_guest(request):
    return render(request, "room_subuser.html")




