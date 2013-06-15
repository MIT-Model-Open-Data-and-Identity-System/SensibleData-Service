from django.db import models
from django.contrib.auth.models import User

SCOPE_LENGTH = 255
CODE_KEY_LENGTH = 30
REFRESH_TOKEN_LENGTH = 10
ACCESS_TOKEN_LENGTH = 10


class PlatformScope(models.Model):
    """Stores scope to be used between service and platform.

    **Args:**

    * *key:* A string representing the access range scope. Used in access
      token requests.

    **Kwargs:**

    * *description:* A string representing the access range description.
      *Default None*

    """
    key = models.CharField(unique=True, max_length=SCOPE_LENGTH, db_index=True)
    description = models.TextField(blank=True)


class PlatformCode(models.Model):
    """Stores authorization code data.

    **Args:**

    * *client:* A oauth2app.models.Client object
    * *user:* A django.contrib.auth.models.User object

    **Kwargs:**

    * *key:* A string representing the authorization code. *Default 30
      character random string*
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None*

    """
    user = models.ForeignKey(User)
    code = models.CharField(
        unique=True,
        max_length=CODE_KEY_LENGTH,
        db_index=True)
    scope = models.ManyToManyField(PlatformScope)
    exchanged = models.BooleanField(default=False)
    time_generated = models.PositiveIntegerField()
    time_exchanged = models.PositiveIntegerField(null=True)


class PlatformAccessToken(models.Model):
    user = models.ForeignKey(User)
    code = models.ForeignKey(PlatformCode)
    token = models.CharField(
        unique=True,
        max_length=ACCESS_TOKEN_LENGTH,
        db_index=True)
    token_type = models.CharField(max_length=100)
    refresh_token = models.CharField(
        unique=True,
        blank=True,
        null=True,
        max_length=REFRESH_TOKEN_LENGTH,
        db_index=True)
    expire = models.PositiveIntegerField()
    scope = models.ManyToManyField(PlatformScope)
