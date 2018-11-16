# -*- coding: utf-8 -*-
from django.conf.urls import url
from GameAssistant.consumers import gameConsumer, TestConsumer

def message_handler(message):
    print(message['text'])

websocket_urlpatterns = [
    url(r'^ws/$', gameConsumer),
    url(r'^test/$', TestConsumer),
]