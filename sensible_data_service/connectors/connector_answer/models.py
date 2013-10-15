from django.db import models
from connectors.models import *


class ConnectorAnswer(Connector):
	class Meta:
		app_label = 'connectors'
