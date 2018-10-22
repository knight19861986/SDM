# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
import re
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from GameAssistant.libs.utils import check_auth, game_ongoing, get_client_id_from_session
from GameAssistant.libs.enums import SeatState
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

        #If no cookie of subclient:
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


def _subclient_is_seated(subclient, game):
    for seat in game.game_seats:
        if seat.user_id == subclient.subclient_id:
            return True
    return False


@game_ongoing('yes', 'subuser')
def sit(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')
    try:
        game_code = request.POST.get('game_code')
        seat_number = request.POST.get('seat_number')
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        subclient_id = session.get_decoded().get('subclient_id')
        client_id = subclient_id.split('@',1)[-1]

        client = Client.objects(client_id=client_id).first()
        subclient = client.subclients.filter(subclient_id=subclient_id).first()
        game = Game.objects(game_code=game_code).first()

        if not _subclient_is_seated(subclient, game):
            seat = game.game_seats.filter(seat_number=seat_number).first()
            current_seat_state = seat.seat_state
            if current_seat_state == SeatState.empty.value:
                if game.update_seat(seat_number=seat_number, user_id=subclient_id, seat_state=SeatState.subuser.value):
                    url = reverse('GameAssistant:going_room_guest')
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponseBadRequest("Unknown error happened! Failed to update game!")

        url = reverse('GameAssistant:going_room_guest')
        return HttpResponseRedirect(url)

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running subclient.sit! Details: {0}'.format(e))

@game_ongoing('yes', 'subuser')
def unsit(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')
    try:
        game_code = request.POST.get('game_code')
        seat_number = request.POST.get('seat_number')
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        subclient_id = session.get_decoded().get('subclient_id')
        client_id = subclient_id.split('@',1)[-1]

        client = Client.objects(client_id=client_id).first()
        subclient = client.subclients.filter(subclient_id=subclient_id).first()
        game = Game.objects(game_code = game_code).first()

        if _subclient_is_seated(subclient, game):            
            seat = game.game_seats.filter(seat_number=seat_number).first()
            current_seat_state = seat.seat_state
            current_seat_user_id = seat.user_id
            if (current_seat_state != SeatState.empty.value) and (current_seat_user_id == subclient_id):
                if game.update_seat(seat_number=seat_number, user_id='', seat_state=SeatState.empty.value):
                    url = reverse('GameAssistant:going_room_guest')
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponseBadRequest("Unknown error happened! Failed to update game!")

        url = reverse('GameAssistant:going_room_guest')
        return HttpResponseRedirect(url)

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running subclient.unsit! Details: {0}'.format(e))

