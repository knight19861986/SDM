# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
import re
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from GameAssistant.libs.utils import check_auth, game_ongoing, get_client_id_from_session
from django.shortcuts import render

@check_auth('guest')
def enter(request):
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

        client = Client.objects(client_id = client_id).first()

        if 'sessionid' in request.COOKIES:
            sessionid = request.COOKIES.get('sessionid')
            session = Session.objects.get(session_key=sessionid)
            if session and session.get_decoded().get('subclient_id'):
                subclient_id = session.get_decoded().get('subclient_id')
                if client.has_subclient(subclient_id):

                    url = reverse('GameAssistant:going_room_guest')
                    return HttpResponseRedirect(url)

        #if no cookie of subclient:
        subclient_id = client.generate_subclient_id()
        if client.add_subclient(subclient_id = subclient_id):
            request.session.set_expiry(60*60*24) 
            request.session['subclient_id'] = subclient_id

            url = reverse('GameAssistant:going_room_guest')
            return HttpResponseRedirect(url)

        else:
            return HttpResponseBadRequest('Unknown error happened! Failed to generate subuser!')


    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running subclient.enter! Details: {0}'.format(e))


@game_ongoing('yes', 'subuser')
def sit(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')
    try:
        # game_code = request.POST.get('game_code')
        # print(game_code)
        # seat_number = request.POST.get('seat_number')
        # print(seat_number)
        # game = Game.objects(game_code = game_code).first()
        # game.update_seat(seat_number=seat_number)

        return HttpResponse('View of subclient.sit() is on the way!')


    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running seat.sit_subclient! Details: {0}'.format(e))

@game_ongoing('yes', 'subuser')
def unsit(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')
    try:

        return HttpResponse('View of subclient.unsit() is on the way!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running seat.sit_subclient! Details: {0}'.format(e))


