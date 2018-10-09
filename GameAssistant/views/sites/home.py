# -*- coding: utf-8 -*-

from GameAssistant.libs.utils import check_auth
from django.shortcuts import render

@check_auth('guest')
def index(request, errorcode):
    messages = {
        '0': "Illegal game code!",
        '1': "Game code is not existed!",
        '2': "Unexpected error happen! The host of the game is missing! Please try with another code!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''

    return render(request, "home.html", {'error_msg': msg})

############### Remove later #################
def tab(request):
    return render(request, "tab_example.html")
##############################################

@check_auth('guest')
def sign_up(request, errorcode):
    messages = {
        '0': "User name has already existed!",
        '1': "Illegal password!",
        '2': "Illegal username!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''

    return render(request, "sign_up.html", {'error_msg': msg})

@check_auth('guest')
def sign_up_success(request):
    return render(request, "sign_up_success.html")

@check_auth('guest')
def sign_in(request, errorcode):
    messages = {
        '0': "User name is not existed!",
        '1': "Wrong password!"
    }
    if errorcode in messages:
        msg = messages.get(errorcode)
    else:
        msg =''
    return render(request, "sign_in.html", {'error_msg': msg})

