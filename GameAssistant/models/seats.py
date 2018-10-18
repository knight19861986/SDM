# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *
from GameAssistant.libs.enums import SeatState 

class Seat(EmbeddedDocument):
    
    seat_number = IntField(default = 0, required=True)
    game_code = StringField(max_length = 200, required=True)
    seat_state = IntField(default = 0, required=True)
    subuser_id = StringField(max_length = 200, default = None)
    nickname = StringField(max_length = 200, default = None)
    time_created = DateTimeField(default = datetime.now)
    time_modified = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            'game_code',
            'subuser_id'

        ]
    }

    def __unicode__(self):
        return self.room_number
