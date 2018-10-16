from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.games import Game
from GameAssistant.libs.utils import check_auth, game_ongoing
from django.shortcuts import render

@game_ongoing('yes', 'superuser')
def room(request):
    return render(request, "room_superuser.html")


@check_auth('subuser')
def room_guest(request):
    return render(request, "room_subuser.html")




