# -*- coding: utf-8 -*-
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class gameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'Name1'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'logging',
                'message': 'Refresh'
            }
        )

    def logging(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(text_data)