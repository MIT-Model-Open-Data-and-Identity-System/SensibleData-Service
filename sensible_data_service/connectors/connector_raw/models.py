from django.db import models
from connectors.models import *


class ConnectorRaw(Connector):
	class Meta:
		app_label = 'connectors'
