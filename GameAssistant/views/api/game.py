# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from datetime import datetime
import re
#from mongoengine import *
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.games import Game
from GameAssistant.models.seats import Seat
from GameAssistant.libs.utils import check_auth, game_ongoing

@check_auth('superuser')
@game_ongoing('no')
def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')

    try:
        game_code = request.POST.get('game_code')

        if not re.match("^[A-Za-z0-9]*$", game_code):
            url = reverse('GameAssistant:start_new', args=[1])
            return HttpResponseRedirect(url)
        if Game.objects(game_code = game_code):
            url = reverse('GameAssistant:start_new', args=[0])
            return HttpResponseRedirect(url)

        num_of_players = request.POST.get('num_of_players')

        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')

        room_number = 0
        while True:
            room_number += 1
            if not Game.objects(room_number=room_number):
                break

        game = Game(client_id=client_id, room_number=room_number, game_code=game_code, num_of_players=num_of_players)
        for number in range(1, game.num_of_players+1):
            seat = Seat(seat_number=number, game_code=game_code)
            game.game_seats.append(seat)
        game.save()
    
        url = reverse('GameAssistant:going_room')
        return HttpResponseRedirect(url)

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.create! Details: {0}'.format(e))


@check_auth('superuser')
@game_ongoing('yes')
def get_seats(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ret = []
            for seat in game.game_seats:
                ret.append({
                    'SeatNumber': seat.seat_number,
                    'NickName': seat.subuser_name if seat.subuser_name else 'Waiting',

                    })

            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_game! Details: {0}'.format(e))


@check_auth('superuser')
@game_ongoing('yes')
def get_game(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ret = {}
            ret['Room number'] = game.room_number
            ret['Game code'] = game.game_code
            ret['Number of players'] = game.num_of_players
            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_game! Details: {0}'.format(e))


@check_auth('superuser')
@game_ongoing('yes')
def delete(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            game.delete()
        url = reverse('GameAssistant:start_profile', args=[''])
        return HttpResponseRedirect(url)
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.delete! Details: {0}'.format(e))



