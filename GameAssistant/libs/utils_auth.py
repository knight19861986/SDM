# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from django.urls import reverse
from GameAssistant.libs.enums import GameState
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from django.contrib.sessions.models import Session

def check_auth(auth_level):
    def _check_auth(func):
        def wrapper(request, *callback_args, **callback_kwargs):
            try:
                if auth_level == 'superuser':
                    if 'sessionid' in request.COOKIES:
                        sessionid = request.COOKIES.get('sessionid')
                        session = Session.objects.get(session_key=sessionid)
                        if session and session.get_decoded().get('client_id'):
                            return func(request, *callback_args, **callback_kwargs)
                        else:
                            return HttpResponseForbidden('Session of superuser not existed! Please sign in again!')
                    else:
                        url = reverse('GameAssistant:home_index', args=[''])
                        return HttpResponseRedirect(url)

                elif auth_level == 'subuser':
                    if 'sessionid' in request.COOKIES:
                        sessionid = request.COOKIES.get('sessionid')
                        session = Session.objects.get(session_key=sessionid)
                        if session and session.get_decoded().get('client_id'):
                            url = reverse('GameAssistant:start_profile', args=[''])
                            return HttpResponseRedirect(url)
                        elif session and session.get_decoded().get('subclient_id'):
                            #Need to check if the client has this subclient!
                            subclient_id = session.get_decoded().get('subclient_id')
                            client_id = subclient_id.split('@',1)[-1]
                            client = Client.objects(client_id = client_id).first()
                            if client:
                                if client.has_subclient(subclient_id):
                                    return func(request, *callback_args, **callback_kwargs)
                                else:
                                    url = reverse('GameAssistant:home_index', args=['3'])
                                    return HttpResponseRedirect(url)
                            else:
                                url = reverse('GameAssistant:home_index', args=['4'])
                                return HttpResponseRedirect(url)
                        return HttpResponseForbidden('Session of subuser expired! Please join a game again!')

                    else:
                        url = reverse('GameAssistant:home_index', args=[''])
                        return HttpResponseRedirect(url)

                elif auth_level == 'user':
                    if 'sessionid' in request.COOKIES:
                        sessionid = request.COOKIES.get('sessionid')
                        session = Session.objects.get(session_key=sessionid)
                        if session:
                            if session.get_decoded().get('client_id') or session.get_decoded().get('subclient_id'):
                                return func(request, *callback_args, **callback_kwargs)
                        return HttpResponseForbidden('Session not existed!')
                    else:
                        url = reverse('GameAssistant:home_index', args=[''])
                        return HttpResponseRedirect(url)

                elif auth_level == 'guest':
                    if 'sessionid' in request.COOKIES:
                        sessionid = request.COOKIES.get('sessionid')
                        session = Session.objects.get(session_key=sessionid)
                        if session and session.get_decoded().get('client_id'):
                            url = reverse('GameAssistant:start_profile', args=[''])
                            return HttpResponseRedirect(url)
                    return func(request, *callback_args, **callback_kwargs)
                else:
                    return HttpResponseBadRequest('Illegal authentication level!')
            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.check_auth! Details: {0}'.format(e))
        return wrapper
    return _check_auth


def check_game_state(state_codes, auth_level):
    def _check_game_state(func):
        @check_auth(auth_level)
        def wrapper(request, *callback_args, **callback_kwargs):
            try: 
                sessionid = request.COOKIES.get('sessionid')
                session = Session.objects.get(session_key=sessionid)
                if auth_level == 'subuser':
                    subclient_id = session.get_decoded().get('subclient_id')
                    client_id = subclient_id.split('@',1)[-1]
                elif auth_level == 'superuser':
                    client_id = session.get_decoded().get('client_id')
                else:
                    return HttpResponseBadRequest('Illegal request becuase of illegal authentication level!')

                if not state_codes:
                    if Game.objects(client_id = client_id):
                        url = reverse('GameAssistant:start_profile', args=['0'])
                        return HttpResponseRedirect(url)                            
                else:
                    if not Game.objects(client_id = client_id):
                        url = reverse('GameAssistant:start_profile', args=['1'])
                        return HttpResponseRedirect(url)
                    else:
                        game = Game.objects(client_id = client_id).first()
                        if not (game.game_state & state_codes):
                            return HttpResponseBadRequest('Illegal request becuase of illegal game state!')
                return func(request, *callback_args, **callback_kwargs)

            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.game_state! Details: {0}'.format(e))
        return wrapper
    return _check_game_state
