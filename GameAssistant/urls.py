# -*- coding: utf-8 -*-
from django.conf.urls import url
from GameAssistant.views.sites import home, start, going
from GameAssistant.views.api import board, client, subclient, game

app_name =  "GameAssistant"
urlpatterns = [

    ################ Home ##################
    url(r'^((?P<errorcode>\d)|)$', home.index, name='home_index'),
    # url(r'^tab/$', home.tab, name='tab'), # Remove later
    url(r'^sign-up/((?P<errorcode>\d)|)$', home.sign_up, name='sign_up'),
    url(r'^sign-up/succces/$', home.sign_up_success, name='sign_up_succces'),
    url(r'^sign-in/((?P<errorcode>\d)|)$', home.sign_in, name='sign_in'),

    ################ Start #################
    url(r'^new/((?P<boardname>\w+)|)/((?P<errorcode>\d)|)$', start.new, name='start_new'),
    url(r'^profile/((?P<errorcode>\d)|)$', start.profile, name='start_profile'),

    ############### Going ##################
    url(r'^room/$', going.room, name='going_room'),
    url(r'^room-guest/$', going.room_guest, name='going_room_guest'),

    ################ Board #################
    url(r'^board/ajax_boards/$', board.get_board_list, name='board_list'),
    url(r'^board/ajax_roles/((?P<boardname>\w+)|)$', board.get_board_roles, name='board_roles'),

    ############### Client #################
    url(r'^client/create/$', client.create, name='client_create'),
    url(r'^client/enter/$', client.enter, name='client_enter'),
    url(r'^client/exit/$', client.exit, name='client_exit'),
    url(r'^client/ajax_profile/$', client.get_client, name='client_profile'),
    url(r'^client/sit/$', client.sit, name='client_sit'),
    url(r'^client/unsit/$', client.unsit, name='client_unsit'),
    url(r'^client/remove/$', client.remove, name='client_remove'),
    url(r'^client/rename/$', client.rename, name='client_rename'),
    url(r'^client/edit/$', client.edit, name='client_edit'),

    ############### SubClient ##############
    url(r'^subclient/enter/$', subclient.enter, name='subclient_enter'),
    url(r'^subclient/sit/$', subclient.sit, name='subclient_sit'),
    url(r'^subclient/unsit/$', subclient.unsit, name='subclient_unsit'),
    url(r'^subclient/edit/$', subclient.edit, name='subclient_edit'),


    ############### Game ###################
    url(r'^game/create/$', game.create, name='game_create'),
    url(r'^game/start/$', game.start, name='game_start'),
    url(r'^game/end/$', game.end, name='game_end'),
    url(r'^game/delete/$', game.delete, name='game_delete'),
    url(r'^game/ajax_game_information/$', game.get_game_infor, name='game_information'),
    url(r'^game/ajax_user_information/$', game.get_user_infor, name='game_user'),
    url(r'^game/ajax_seats/$', game.get_seats, name='game_seats'),
]