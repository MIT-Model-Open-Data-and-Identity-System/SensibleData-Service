from django.db import models
from connectors.models import *

from django.contrib.auth.models import User


class ConnectorEconomics(Connector):
    class Meta:
        app_label = 'connectors'


class Voucher(models.Model):
    voucher = models.CharField(max_length=64, unique=True)
    won_by = models.ForeignKey(User, null=True, blank=True, unique=False)
    def __unicode__(self):
        u = ""
        if self.won_by is not None:
            u = " won by "+self.won_by
        return self.voucher+u