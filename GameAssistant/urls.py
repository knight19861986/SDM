from django.conf.urls import url
from GameAssistant.views.sites import home, start, going
from GameAssistant.views.api import client, game

app_name =  "GameAssistant"
urlpatterns = [

	################Home##################
    url(r'^$', home.index, name='home_index'),
    # url(r'^tab/$', home.tab, name='tab'), # Remove later
    url(r'^sign-up/((?P<errorcode>\d)|)$', home.sign_up, name='sign_up'),
    url(r'^sign-up/succces/$', home.sign_up_success, name='sign_up_succces'),
    url(r'^sign-in/((?P<errorcode>\d)|)$', home.sign_in, name='sign_in'),

    ################Start##################
    url(r'^enter/$', start.enter, name='start_enter'),
    url(r'^exit/$', start.exit, name='start_exit'),
    url(r'^new/((?P<errorcode>\d)|)$', start.new, name='start_new'),
    url(r'^profile/((?P<errorcode>\d)|)$', start.profile, name='start_profile'),

    ################Going###################
    url(r'^room/$', going.room, name='going_room'),

	################Client##################
    url(r'^client/create/$', client.create, name='client_create'),
    url(r'^client/ajax_profile/$', client.get_client, name='client_profile'),

    ################Game##################
    url(r'^game/create/$', game.create, name='game_create'),
    url(r'^game/delete/$', game.delete, name='game_delete'),
    url(r'^game/ajax_information/$', game.get_game, name='game_information'),
    url(r'^game/ajax_seats/$', game.get_seats, name='game_seats'),
]