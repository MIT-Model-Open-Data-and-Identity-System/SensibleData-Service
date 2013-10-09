from django.db import models
from connectors.models import *



class ConnectorEconomics(Connector):
    class Meta:
        app_label = 'connectors'
