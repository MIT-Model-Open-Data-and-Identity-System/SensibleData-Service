from django.db import models
from connectors.models import Scope, Connector

class ConnectorAnswer(Connector):
	class Meta:
		app_label = 'connectors'

class ConnectorAnswerEndpoint(models.Model):
	question = models.CharField(max_length=100, db_index=True, help_text="Associated question name")
	answer = models.CharField(unique=True, max_length=100, db_index=True, help_text="Endpoint name")
	scopes = models.ManyToManyField(Scope)
	active = models.BooleanField(default=False)
