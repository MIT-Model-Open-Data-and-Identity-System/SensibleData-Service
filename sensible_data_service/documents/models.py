from django.db import models
from hashlib import sha512
from uuid import uuid4
from django.contrib.auth.models import User


class InformedConsent(models.Model):
	user = models.ForeignKey(User)
	version = models.CharField(max_length=240, db_index=True)
	git_version = models.CharField(max_length=240, db_index=True)
	text_sha512 = models.CharField(max_length=240, db_index=True)
	lang = models.CharField(max_length=240, db_index=True)
	accepted_at = models.PositiveIntegerField(null=True)
