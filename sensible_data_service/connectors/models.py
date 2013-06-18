from django.db import models

class ConnectorManager(models.Manager):
	def get_by_natural_key(self, name):
		return self.get(name=name)

class Connector(models.Model):
	objects = ConnectorManager()

	name = models.CharField(unique=True, max_length=100)
	description = models.TextField(blank=True)
	grant_url = models.URLField(null=True)
	revoke_url = models.URLField(null=True)
	connector_type = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'connectors'


class Scope(models.Model):
	connector = models.ForeignKey(Connector)
	scope = models.CharField(unique=True, max_length=100, db_index=True)
	description = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.scope

