from django.db import models
from django.contrib.auth.models import User

class Participant(models.Model):
	user = models.OneToOneField(User)
	status = models.CharField(max_length=100, blank=True)
