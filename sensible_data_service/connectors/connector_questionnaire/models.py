from django.db import models
from connectors.models import *


class ConnectorQuestionnaire(Connector):
        class Meta:
                app_label = 'connectors'
