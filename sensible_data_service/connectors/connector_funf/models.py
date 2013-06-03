from django.db import models
from connectors.models import *

class File(models.Model):
	filename = models.CharField(max_length=30)

class DatabasePopulationAgent(models.Model): 
	pid = models.CharField(max_length=30)
	last_interaction = models.CharField(max_length=30)
	filenames = models.ManyToManyField(File)
	
class ConnectorFunf(Connector):
	upload_path = models.CharField(max_length=512)
	upload_not_authorized_path = models.CharField(max_length=512)
	decrypted_path = models.CharField(max_length=512)
	decryption_failed_path = models.CharField(max_length=512)
	load_failed_path = models.CharField(max_length=512)
	config_path = models.CharField(max_length=512)
	backup_path = models.CharField(max_length=512)
	
	max_population_processes = models.PositiveIntegerField()
	max_population_files = models.PositiveIntegerField()
	

	class Meta:
                app_label = 'connectors'
