# -*- coding: utf-8 -*-
import time
from datetime import datetime
from mongoengine import *
from GameAssistant.libs.enums import GameState
from GameAssistant.models.seats import Seat

class Game(Document):
    client_id = StringField(max_length = 200, required=True)
    room_number = IntField(default = 0)
    game_code = StringField(max_length = 200, required=True)
    board_name = StringField(max_length = 200, required=True)
    game_state = IntField(default = GameState.preparing.value)
    num_of_players = IntField(default = 4, required=True)
    time_created = DateTimeField(default = datetime.now)
    _timestamp = IntField(default = int(time.time()*1000000))

    game_seats = EmbeddedDocumentListField(Seat)

    meta = {
        'indexes': [
            'client_id',
            'room_number',
            'game_code'

        ]
    }

    def websocket_id(self):
        return 'room_' + str(self.room_number) + '_' + str(int(self._timestamp))

    def update_seat(self, seat_number, **kwargs):
        seat = self.game_seats.filter(seat_number = seat_number).first()
        seat.time_modified = datetime.now
        for key, value in kwargs.items():
            if hasattr(seat, key):
                setattr(seat, key, kwargs[key])
        try:
            self.save()
            return True
        except:
            return False

    def is_ready(self):
        for seat in self.game_seats:
            if not seat.seat_state:
                return False
        return True


    def __str__(self):
        return self.game_code
