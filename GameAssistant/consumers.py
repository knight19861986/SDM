# -*- coding: utf-8 -*-
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['ws_id']
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_id,
            self.channel_name
        )

    def refeshing(self, event):
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

