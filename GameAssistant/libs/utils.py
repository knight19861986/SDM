# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest,HttpResponseForbidden
from django.urls import reverse
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.models.games import Game
from django.contrib.sessions.models import Session

from GameAssistant.libs.utils_precheck import check_auth # To remove


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


#Works for both super_user and sub_user
def user_is_seated(user_id, game):
    for seat in game.game_seats:
        if seat.user_id == user_id:
            return True
    return False

