# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.libs.utils import check_auth, game_ongoing
from django.shortcuts import render

@check_auth('guest')
def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')


    try:
        game_code = request.POST.get('gamecode')

        return 0


    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running subclient.create! Details: {0}'.format(e))

