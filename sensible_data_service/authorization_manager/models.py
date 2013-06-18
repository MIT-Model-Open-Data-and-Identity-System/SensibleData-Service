from django.db import models
from django.contrib.auth.models import User
from connectors.models import *
from application_manager.models import *
from oauth2app.models import AccessToken, TimestampGenerator, KeyGenerator

class Authorization(models.Model):
	user = models.ForeignKey(User)
	scope = models.ForeignKey(Scope)
	application = models.ForeignKey(Application)
	payload = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=False)
	created_at = models.PositiveIntegerField(editable=False, default=TimestampGenerator())
	activated_at = models.PositiveIntegerField(null=True)
	revoked_at = models.PositiveIntegerField(null=True)
	access_token = models.ForeignKey(AccessToken, null=True)
	nonce = models.CharField(null=True, blank=True, max_length=100, default=KeyGenerator(10))
