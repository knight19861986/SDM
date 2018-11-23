# -*- coding: utf-8 -*-
import time
from datetime import datetime
from mongoengine import *
from GameAssistant.models.subclients import SubClient

class Client(Document):
    client_id = StringField(max_length = 200, required=True)
    client_name = StringField(max_length = 200)
    client_email = EmailField(default=None)
    pin = StringField(max_length = 200)
    _subuser_counter = IntField(default = 0)
    time_created = DateTimeField(default=datetime.now)
    time_modified = DateTimeField(default=datetime.now)

    subclients = EmbeddedDocumentListField(SubClient)

    meta = {
        'indexes': [
            {
                'fields': ['client_id'],
                'expireAfterSeconds': 3600
            }
        ]
    }

    def generate_subclient_id(self):
        timestamp = time.time()
        return 'friend' + str(int(timestamp*1000000)) + '@' +self.client_id

    def _get_next_subclient_name(self):
        self._subuser_counter += 1
        if self._subuser_counter > 1000:
            self._subuser_counter = 1
        return 'Friend No.' + str(self._subuser_counter)

    def add_subclient(self, **kwargs):
        subclient_name = self._get_next_subclient_name()
        subclient_id = kwargs['subclient_id'] if 'subclient_id' in kwargs else self.generate_subclient_id()
        subclient = SubClient(subclient_id = subclient_id, subclient_name = subclient_name)
        self.subclients.append(subclient)
        try:
            self.save()
            return True
        except:
            return False

    def update_subclient(self, subclient_id, **kwargs):
        subclient = self.subclients.filter(subclient_id = subclient_id).first()
        subclient.time_modified = datetime.now
        for key, value in kwargs.items():
            if hasattr(subclient, key):
                setattr(subclient, key, kwargs[key])
        try:
            self.save()
            return True
        except:
            return False

    def has_subclient(self, subclient_id):
        subclient = self.subclients.filter(subclient_id = subclient_id)
        if subclient:
            return True
        else:
            return False

    def clear_subclients(self):
        self.subclients.delete()
        self._subuser_counter = 0
        try:
            self.save()
            return True
        except:
            return False


    def __str__(self):
        return self.client_id
