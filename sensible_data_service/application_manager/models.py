from django.db import models
from hashlib import sha512
from uuid import uuid4
from django.contrib.auth.models import User
from connectors.models import *

class KeyGenerator(object):
    """Callable Key Generator that returns a random keystring.

    **Args:**

    * *length:* A integer indicating how long the key should be.

    *Returns str*
    """
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]

class Parameter(models.Model):
	key = models.CharField(max_length=240, db_index=True)
	value = models.CharField(max_length=240, db_index=True)
	def __unicode__(self):
		return self.key+':'+self.value

class Application(models.Model):
	name = models.CharField(unique=True, max_length=256)
	_id = models.CharField(unique=True, max_length=20, default=KeyGenerator(20), db_index=True)
	user = models.ForeignKey(User)
	scopes = models.ManyToManyField(Scope)
	params = models.ManyToManyField(Parameter)
	description = models.TextField(null=True, blank=True)
	connector_type = models.CharField(max_length=100)
