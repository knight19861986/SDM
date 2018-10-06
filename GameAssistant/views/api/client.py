# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from datetime import datetime
import re
#from mongoengine import *
from django.contrib.sessions.models import Session
from GameAssistant.models.clients import Client
from GameAssistant.models.subclients import SubClient
from GameAssistant.libs.utils import check_auth

@check_auth('guest')
def create(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST are allowed!')

    try:
        client_id = request.POST.get('username')
        client_name = request.POST.get('username') 
        pin = request.POST.get('password')

        if not re.match("^[A-Za-z0-9]*$", client_id):
            url = reverse('GameAssistant:sign_up', args=[2])
            return HttpResponseRedirect(url)

        if not re.match("^[A-Za-z0-9!@#$%ˆ&*():;<>,.]*$", pin):
            url = reverse('GameAssistant:sign_up', args=[1])
            return HttpResponseRedirect(url)

        if Client.objects(client_id = client_id):
            url = reverse('GameAssistant:sign_up', args=[0])
            return HttpResponseRedirect(url)

        client = Client(client_id = client_id, client_name = client_name, pin = pin)
        client.save()

        # response = '<script>alert(\'Succeed to send!\')</script>'
        # return HttpResponse(response)
        url = reverse('GameAssistant:sign_up_succces')
        return HttpResponseRedirect(url)

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running client.create! Details: {0}'.format(e))

@check_auth('superuser')
def get_client(request):
    try:
        sessionid = request.COOKIES.get('sessionid')
        session = Session.objects.get(session_key=sessionid)
        client_id = session.get_decoded().get('client_id')
        if Client.objects(client_id = client_id):
            client = Client.objects(client_id = client_id).first()
            ret = {}
            ret['Id'] = client.client_id
            ret['Name'] = client.client_name if client.client_name else ''
            ret['Email'] = client.client_email if client.client_email else ''
            ret['Registered Time'] = client.time_created

            return JsonResponse(ret, safe=False)

        return HttpResponseBadRequest('Client not existed!')

    except Exception as e:
        return HttpResponseBadRequest('Unknown error while running client.get_client! Details: {0}'.format(e))






