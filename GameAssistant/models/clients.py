# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *
from GameAssistant.models.subclients import SubClient

class Client(Document):
    client_id = StringField(max_length = 200, required=True)
    client_name = StringField(max_length = 200)
    client_email = EmailField(default=None)
    pin = StringField(max_length = 200)
    time_created = DateTimeField(default=datetime.now)
    time_modified = DateTimeField(default=datetime.now)

    subclients = ListField(EmbeddedDocumentField(SubClient))

    meta = {
        'indexes': [
            {
                'fields': ['client_id'],
                'expireAfterSeconds': 3600
            }
        ]
    }


    def add_subclient(self):
        no_of_subuser = len(self.subclients) + 1
        subclient_name = 'Friend No.' + str(no_of_subuser)
        subclient_id = 'friend' + str(no_of_subuser) + '@' +self.client_id
        subclient = SubClient(subclient_id = subclient_id, subclient_name = subclient_name)
        self.subclients.append(subclient)
        try: 
            self.save()
            new_client_id = subclient_id.split('@',1)[-1]
            print(new_client_id)
            return True
        except:
            return False


    def __unicode__(self):
        return self.client_id
