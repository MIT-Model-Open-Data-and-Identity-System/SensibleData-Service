from django.db import models
from django.contrib.auth.models import User
from connectors.models import *
from application_manager.models import *

class Authorization(models.Model):
	user = models.ForeignKey(User)
	scope = models.ForeignKey(Scope)
	application = models.ForeignKey(Application)
	payload = models.TextField(null=True, blank=True)
	active = models.BooleanField()
	created_at = models.PositiveIntegerField(null=True)
	revoked_at = models.PositiveIntegerField(null=True)

class GcmRegistration(models.Model):
	user = models.ForeignKey(User)
	device_id = models.CharField(max_length=256)
	gcm_id = models.CharField(max_length=256)
	
