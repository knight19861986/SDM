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
from GameAssistant.libs.utils import user_is_seated, get_user_role
from GameAssistant.libs.utils_precheck import check_auth, check_game_state
from GameAssistant.libs.utils_session import *
from GameAssistant.libs.utils_websocket import ws_push
from GameAssistant.libs.utils_board import board_factory
from GameAssistant.libs.enums import GameState, SeatState, RefreshType

@check_game_state(GameState.no.value, 'superuser')
def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')

    try:
        game_code = request.POST.get('game_code')
        board_name = request.POST.get('board_name')

        if not re.match("^[A-Za-z0-9]*$", game_code):
            url = reverse('GameAssistant:start_new', args=[board_name, 1])
            return HttpResponseRedirect(url)
        if Game.objects(game_code = game_code):
            url = reverse('GameAssistant:start_new', args=[board_name, 0])
            return HttpResponseRedirect(url)

        num_of_players = int(request.POST.get('num_of_players'))
        board_name = request.POST.get('board_name')
        board = board_factory(board_name)
        role_config={}
        for key,value in request.POST.items():
            if key in board.role_index:
                role_config[key] = int(value)

        board.set_role_config(role_config)
        role_list = board.deal()

        if len(role_list) != num_of_players:
            url = reverse('GameAssistant:start_new', args=[board_name, 2])
            return HttpResponseRedirect(url)

        client_id = get_client_id_from_session(request)
        room_number = 0
        while True:
            room_number += 1
            if not Game.objects(room_number=room_number):
                break

        game = Game(client_id=client_id, room_number=room_number, board_name=board_name, game_code=game_code, num_of_players=num_of_players)
        for number in range(0, game.num_of_players):
            seat = Seat(seat_number=number+1, game_code=game_code, role=role_list[number])
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
            user_seated = 1 if user_is_seated(user_id, game) else 0
            ret = []
            for seat in game.game_seats:
                nickname = 'Waiting'
                user_seated_here = False
                if seat.seat_state == SeatState.superuser.value:
                    nickname = Client.objects(client_id=seat.user_id).first().client_name
                    if client_id == user_id:
                        user_seated_here = True
                elif seat.seat_state == SeatState.subuser.value:
                    nickname = Client.objects(client_id=client_id).first().subclients.filter(subclient_id=seat.user_id).first().subclient_name
                    if user_id == seat.user_id:
                        user_seated_here = True
                ret_single = {
                    'SeatNumber': seat.seat_number,
                    'GameCode': game.game_code,
                    'GameState': game.game_state,
                    'SeatState': seat.seat_state,
                    'NickName': nickname,
                    'UserSeated': user_seated,
                    'UserSeatedHere': user_seated_here
                    }
                if game.game_state & GameState.ended.value:
                    ret_single.update({'Role': seat.role})
                ret.append(ret_single)

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
            ret['BoardName'] = game.board_name
            ret['GameCode'] = game.game_code
            ret['GameState'] = game.game_state
            ret['NumberOfPlayers'] = game.num_of_players
            ret['WsId'] = game.websocket_id()
            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_game_infor! Details: {0}'.format(e))


@check_auth('user')
def get_user_infor(request):
    try:
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ret = {}
            ret['UserName'] = get_user_name_from_session(request)
            ret['GameState'] = game.game_state
            if game.game_state & (GameState.started.value + GameState.ended.value):
                role = get_user_role(get_user_id_from_session(request), game)
                description = board_factory(game.board_name).get_description(role)
                ret['Role'] = role
                ret['Description'] = description

            return JsonResponse(ret, safe=False)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.get_user_infor! Details: {0}'.format(e))


@ws_push('refreshing', RefreshType.seat.value+RefreshType.gamestate.value) 
@check_game_state(GameState.preparing.value, 'superuser')
def start(request):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest('Only POST are allowed!')
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            if(game.is_ready()):
                game.update(game_state = GameState.started.value)
            url = reverse('GameAssistant:going_room')
            return HttpResponseRedirect(url)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.start! Details: {0}'.format(e))


@ws_push('refreshing', RefreshType.seat.value+RefreshType.gamestate.value)
@check_game_state(GameState.started.value, 'superuser')
def end(request):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest('Only POST are allowed!')
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            game.update(game_state = GameState.ended.value)
            url = reverse('GameAssistant:going_room')
            return HttpResponseRedirect(url)
        return HttpResponseBadRequest('Game not existed!')
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running game.end! Details: {0}'.format(e))


@ws_push('refreshing', RefreshType.room.value)
@check_game_state(GameState.preparing.value+GameState.started.value+GameState.ended.value, 'superuser')
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



