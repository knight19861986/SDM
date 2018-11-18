# -*- coding: utf-8 -*-
# Maybe to refactor: change "utils.py" to "utils_auth.py"
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from django.urls import reverse
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from django.contrib.sessions.models import Session


def decorator_example(args):
    def _decorator_example(func):
        def wrapper(request, *callback_args, **callback_kwargs):
            try:
                if not args:
                    return func(request, *callback_args, **callback_kwargs)
                else:
                    return HttpResponseForbidden("Forbidden!")
            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.decorator_example! Details: {0}'.format(e))
        return wrapper
    return _decorator_example


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
                        else:
                            return func(request, *callback_args, **callback_kwargs)
                    else:
                        return func(request, *callback_args, **callback_kwargs)

                else:
                    return HttpResponseBadRequest('Illegal authentication level!')
            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.check_auth! Details: {0}'.format(e))
        return wrapper
    return _check_auth


def game_ongoing(yes_or_no, auth_level):
    def _game_ongoing(func):
        @check_auth(auth_level)
        def wrapper(request, *callback_args, **callback_kwargs):
            try: 
                sessionid = request.COOKIES.get('sessionid')
                session = Session.objects.get(session_key=sessionid)
                if auth_level == 'superuser':
                    client_id = session.get_decoded().get('client_id')
                    if yes_or_no == 'yes':
                        if not Game.objects(client_id = client_id):
                            url = reverse('GameAssistant:start_profile', args=['1'])
                            return HttpResponseRedirect(url)
                        else:
                            return func(request, *callback_args, **callback_kwargs)
                    elif yes_or_no == 'no':
                        if Game.objects(client_id = client_id):
                            url = reverse('GameAssistant:start_profile', args=['0'])
                            return HttpResponseRedirect(url)
                        else:
                            return func(request, *callback_args, **callback_kwargs)

                if auth_level == 'subuser':
                    subclient_id = session.get_decoded().get('subclient_id')
                    client_id = subclient_id.split('@',1)[-1]
                    if yes_or_no == 'yes':
                        if not Game.objects(client_id = client_id):
                            url = reverse('GameAssistant:home_index', args=['3'])
                            return HttpResponseRedirect(url)
                        else:
                            return func(request, *callback_args, **callback_kwargs)
                    elif yes_or_no == 'no':
                        if Game.objects(client_id = client_id):
                            url = reverse('GameAssistant:home_index', args=['2'])
                            return HttpResponseRedirect(url)
                        else:
                            return func(request, *callback_args, **callback_kwargs)

                return HttpResponseBadRequest('Illegal argument in utils.game_ongoing!')

            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.game_ongoing! Details: {0}'.format(e))
        return wrapper
    return _game_ongoing


#Works for both super_user and sub_user
def user_is_seated(user_id, game):
    for seat in game.game_seats:
        if seat.user_id == user_id:
            return True
    return False
