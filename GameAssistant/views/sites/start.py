# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.libs.utils import check_auth, game_ongoing
from django.shortcuts import render

@check_auth('guest')
def enter(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed')
    try:
        client_id = request.POST.get('username')
        pin = request.POST.get('password')
        client = Client.objects(client_id= client_id)

        if not client:
            url = reverse('GameAssistant:sign_in', args=[0])
            return HttpResponseRedirect(url)

        elif not pin == client.get().pin:
            url = reverse('GameAssistant:sign_in', args=[1])
            return HttpResponseRedirect(url)

        else:
            request.session['client_id'] = client_id
            url = reverse('GameAssistant:start_profile', args=[''])
            return HttpResponseRedirect(url)
    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running start.enter! Details: {0}'.format(e))

@check_auth('superuser')
def exit(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed')
    if 'client_id' in request.session:
        request.session.flush()
        url = reverse('GameAssistant:sign_in', args=[''])
        return HttpResponseRedirect(url)

    return HttpResponseBadRequest('Unknown error while running start.exit!')


@game_ongoing('no', 'superuser')
def new(request, errorcode):
    messages = {
        '0': "Game code has already existed!",
        '1': "Illegal game code!",
        '2': "You don't have an on-going game, please create a new one first!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''
    return render(request, "initiate.html", {'error_msg': msg})


@check_auth('superuser')
def profile(request, errorcode):
    messages = {
        '0': "You have already started a game!\nPlease close the previous game before you start a new one!",
        '1': "You don't have an on-going game!\nPlease create a new one!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''
    return render(request, "profile.html", {'error_msg': msg})




