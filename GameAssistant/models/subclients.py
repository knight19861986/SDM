# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *

class SubClient(EmbeddedDocument):
    subclient_id = StringField(max_length = 200)
    subclient_name = StringField(max_length = 200)
    time_created = DateTimeField(default=datetime.now)
    time_modified = DateTimeField(default=datetime.now)

    meta = {
        'indexes': [
            {
                'fields': ['subclient_id'],
                'expireAfterSeconds': 3600
            }
        ]
    }

    def __unicode__(self):
        return self.subclient_id
