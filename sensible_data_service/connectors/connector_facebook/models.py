from django.db import models
from connectors.models import *

class ConnectorFacebook(Connector):
	class Meta:
		app_label = 'connectors'
