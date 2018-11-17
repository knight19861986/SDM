# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest
from GameAssistant.libs.utils import check_auth, game_ongoing
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from django.contrib.sessions.models import Session

#Used for:
#Get the client_id when being logged in as a super-user;
#Get the client_id of its super user when working as a sub-user;
@check_auth('user')
def get_client_id_from_session(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if not client_id:
            subclient_id = session.get_decoded().get('subclient_id')
            client_id = subclient_id.split('@',1)[-1]
            if not client_id: 
                return HttpResponseBadRequest('Unknown error happened! Might be due to expired COOKIES or illegal subclient_id!')
        return client_id

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running utils.get_client_id_from_session! Details: {0}'.format(e))

#Used for:
#Get the client_id when being logged in as a super-user;
#Get the subclient_id when working as a sub-user;
@check_auth('user')
def get_user_id_from_session(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if not client_id:
            subclient_id = session.get_decoded().get('subclient_id')
            return subclient_id
        return client_id

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running utils.get_user_id_from_session! Details: {0}'.format(e))

#Used for:
#Get the client_name when being logged in as a super-user;
#Get the subclient_name when working as a sub-user;
@check_auth('user')
def get_user_name_from_session(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if not client_id:
            subclient_id = session.get_decoded().get('subclient_id')
            client_id = subclient_id.split('@',1)[-1]
            subclient = Client.objects(client_id=client_id).first().subclients.filter(subclient_id=subclient_id).first()
            return subclient.subclient_name
        else:
            client = Client.objects(client_id=client_id).first()
            return client.client_name

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running utils.get_user_name_from_session! Details: {0}'.format(e))

#Used for:
#Get the websocket id of the on-going game;
#Return empty string if no game is on-going;
@check_auth('user')
def get_ws_id_from_session(request):
    try:
        client_id = get_client_id_from_session(request)
        if Game.objects(client_id = client_id):
            game = Game.objects(client_id = client_id).first()
            ws_id = game.websocket_id()
            return ws_id
        else:
            return ''

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running utils.get_ws_id_from_session! Details: {0}'.format(e))