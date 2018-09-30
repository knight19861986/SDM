# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *

class Seat(EmbeddedDocument):
    
    seat_number = IntField(default = 0, required=True)
    game_code = StringField(max_length = 200, required=True)
    subuser_id = StringField(max_length = 200, default = None)
    subuser_name = StringField(max_length = 200, default = None)
    time_created = DateTimeField(default = datetime.now)

    meta = {
        'indexes': [
            'game_code',
            'subuser_id'

        ]
    }

    def __unicode__(self):
        return self.room_number
