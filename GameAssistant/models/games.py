# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *
from GameAssistant.models.seats import Seat

class Game(Document):
    client_id = StringField(max_length = 200, required=True)
    room_number = IntField(default = 0)
    game_code = StringField(max_length = 200, required=True)
    num_of_players = IntField(default = 4, required=True)
    time_created = DateTimeField(default = datetime.now)

    game_seats = EmbeddedDocumentListField(Seat)

    meta = {
        'indexes': [
            'client_id',
            'room_number',
            'game_code'

        ]
    }


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

    def __unicode__(self):
        return self.game_code
