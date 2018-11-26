# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *
from GameAssistant.libs.enums import SeatState 

class Seat(EmbeddedDocument):
    
    seat_number = IntField(default = 0, required=True)
    game_code = StringField(max_length = 200, required=True)
    role = StringField(max_length = 200, default = "", required=True)
    seat_state = IntField(default = SeatState.empty.value)
    user_id = StringField(max_length = 200, default = "")
    time_created = DateTimeField(default = datetime.now)
    time_modified = DateTimeField(default = datetime.now)

    meta = {
        'indexes': [
            'game_code',
            'subuser_id'

        ]
    }

    def __str__(self):
        return self.game_code + '_' + str(self.seat_number)
