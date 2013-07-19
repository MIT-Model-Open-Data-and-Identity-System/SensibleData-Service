from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
	user = models.OneToOneField(User)
	status = models.CharField(max_length=100, blank=True)

class Role(models.Model):
	role = models.CharField(max_length=100, blank=True)
	def __unicode__(self):
		return self.role

class UserRole(models.Model):
	user = models.OneToOneField(User)
	roles = models.ManyToManyField(Role)
