from mongoengine import *

class SubClient(Document):
	subclient_id = StringField(max_length = 200)