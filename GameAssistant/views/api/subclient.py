# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
import re
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from GameAssistant.libs.utils import check_auth, game_ongoing
from django.shortcuts import render

@check_auth('guest')
def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')

    try:
        game_code = request.POST.get('gamecode')

        if not re.match("^[A-Za-z0-9]*$", game_code):
            url = reverse('GameAssistant:home_index', args=[0])
            return HttpResponseRedirect(url)

        if not Game.objects(game_code = game_code):
            url = reverse('GameAssistant:home_index', args=[1])
            return HttpResponseRedirect(url)

        game = Game.objects(game_code = game_code).first()

        client_id = game.client_id

        if not Client.objects(client_id = client_id):
            url = reverse('GameAssistant:home_index', args=[4])
            return HttpResponseRedirect(url)

        #if no cookie of subclient
        client = Client.objects(client_id = client_id).first()

        no_of_subuser = len(client.subclients) + 1

        subclient_name = 'Friend No.' + str(no_of_subuser)
        subclient_id = 'friend' + str(no_of_subuser) + '@' +client_id
        subclient = SubClient(subclient_id = subclient_id, subclient_name = subclient_name)
        client.subclients.append(subclient)
        client.save()

        print(subclient_name)
        print(subclient_id)

        response = '<script>alert(\'Succeed to send!\')</script>'
        return HttpResponse(response)


    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running subclient.create! Details: {0}'.format(e))

