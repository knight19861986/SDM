# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.libs.utils import check_auth, game_ongoing
from django.shortcuts import render

@game_ongoing('no', 'superuser')
def new(request, errorcode):
    messages = {
        '0': "Game code has already existed!",
        '1': "Illegal game code!",
        '2': "You don't have an on-going game, please create a new one first!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''
    return render(request, "initiate.html", {'error_msg': msg})


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




