from django.db import models
from connectors.models import *

class ConnectorSbs2(Connector):
	class Meta:
		app_label = 'connectors'
