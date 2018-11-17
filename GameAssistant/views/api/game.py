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
from GameAssistant.libs.utils import check_auth, game_ongoing, get_client_id_from_session, get_user_id_from_session, get_user_name_from_session
from GameAssistant.libs.enums import SeatState

@game_ongoing('no', 'superuser')
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

        client_id = get_client_id_from_session(request)

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


@check_auth('user')
def get_seats(request):
    try:
        client_id = get_client_id_from_session(request)
        user_id = get_user_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ret = []
            for seat in game.game_seats:
                nickname = 'Waiting'
                user_seated = False
                if seat.seat_state == SeatState.superuser.value:
                    nickname = Client.objects(client_id=seat.user_id).first().client_name
                    if client_id == user_id:
                        user_seated = True
                elif seat.seat_state == SeatState.subuser.value:
                    nickname = Client.objects(client_id=client_id).first().subclients.filter(subclient_id=seat.user_id).first().subclient_name
                    if user_id == seat.user_id:
                        user_seated = True
                ret.append({                    
                    'SeatNumber': seat.seat_number,
                    'GameCode': game.game_code,                    
                    'SeatState': seat.seat_state,
                    'NickName': nickname,
                    'UserSeated': user_seated
                    })

            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_seats! Details: {0}'.format(e))


@check_auth('user')
def get_game_infor(request):
    try:
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ret = {}
            ret['RoomNumber'] = game.room_number
            ret['GameCode'] = game.game_code
            ret['NumberOfPlayers'] = game.num_of_players
            ret['UserName'] = get_user_name_from_session(request) #To be removed
            ret['WsId'] = game.websocket_id()
            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_game! Details: {0}'.format(e))

@check_auth('user')
def get_user_infor(request):
    try:
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ret = {}
            ret['UserName'] = get_user_name_from_session(request)
            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_game! Details: {0}'.format(e))


@game_ongoing('yes', 'superuser')
def delete(request):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest('Only POST are allowed!')
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            game.delete()
            url = reverse('GameAssistant:start_profile', args=[''])
            return HttpResponseRedirect(url)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.delete! Details: {0}'.format(e))



