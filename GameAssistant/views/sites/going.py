from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.games import Game
from GameAssistant.libs.utils import check_auth, game_ongoing
from django.shortcuts import render

@game_ongoing('yes', 'superuser')
def room(request):
    return render(request, "room_superuser.html")


#@check_auth('subuser')
def room_guest(request):
    if 'sessionid' in request.COOKIES:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        if session:
            if session.get_decoded().get('client_id'):
                return render(request, "room_superuser.html")
            elif session.get_decoded().get('subclient_id'):
                return render(request, "room_subuser.html")

        return HttpResponseBadRequest('Valid session not existed! Please sign in or join again!')

    else:
        url = reverse('GameAssistant:home_index', args=[''])
        return HttpResponseRedirect(url)



