# -*- coding: utf-8 -*-
from django.conf.urls import url
from GameAssistant.consumers import RoomConsumer, TestConsumer

def message_handler(message):
    print(message['text'])

websocket_urlpatterns = [
    url(r'^ws/(?P<ws_id>[^/]+)/$', RoomConsumer),
    url(r'^test/$', TestConsumer),
]