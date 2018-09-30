# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *

class Client(Document):
    client_id = StringField(max_length = 200, required=True)
    client_name = StringField(max_length = 200)
    client_email = EmailField(default=None)
    pin = StringField(max_length = 200)
    time_created = DateTimeField(default=datetime.now)
    time_modified = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {
                'fields': ['client_id'],
                'expireAfterSeconds': 3600
            }
        ]
    }

    def __unicode__(self):
        return self.client_id
