from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
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
                            return HttpResponseBadRequest('Session of superuser not existed! Please sign in again!')
                    else:
                        return HttpResponseBadRequest('COOKIES expired! Please sign in again!')

                elif auth_level == 'subuser':
                    if 'sessionid' in request.COOKIES:
                        sessionid = request.COOKIES.get('sessionid')
                        session = Session.objects.get(session_key=sessionid)
                        if session and session.get_decoded().get('client_id'):
                            url = reverse('GameAssistant:start_profile', args=[''])
                            return HttpResponseRedirect(url)
                        elif session and session.get_decoded().get('subclient_id'):
                            return func(request, *callback_args, **callback_kwargs)

                        else:
                            return HttpResponseBadRequest('Session of subuser not existed!')
                    else:
                        return HttpResponseBadRequest('COOKIES expired!')

                elif auth_level == 'user':
                    if 'sessionid' in request.COOKIES:
                        sessionid = request.COOKIES.get('sessionid')
                        session = Session.objects.get(session_key=sessionid)
                        if session:
                            if session.get_decoded().get('client_id') or session.get_decoded().get('subclient_id'):
                                return func(request, *callback_args, **callback_kwargs)
                        return HttpResponseBadRequest('Session not existed!')
                    else:
                        return HttpResponseBadRequest('COOKIES expired!')

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

def decorator_example(args):
    def _decorator_example(func):
        def wrapper(request, *callback_args, **callback_kwargs):
            try:
                if not args:
                    return func(request, *callback_args, **callback_kwargs)
                else:
                    return HttpResponseBadRequest("Bad request!")
            except Exception as e:
                return HttpResponseBadRequest('Unknown error while running utils.decorator_example! Details: {0}'.format(e))
        return wrapper
    return _decorator_example


@check_auth('user')
def get_client_id_from_session(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if not client_id:
            subclient_id = session.get_decoded().get('subclient_id')
            client_id = subclient_id.split('@')[-1]
            if not client_id: 
                return HttpResponseBadRequest('Unknown error happened! Might be due to illigal subclient_id!')
        return client_id

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running utils.get_client_id_from_session! Details: {0}'.format(e))



