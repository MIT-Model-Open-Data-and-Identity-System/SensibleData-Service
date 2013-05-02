from django.db import models

class File(models.Model):
	filename = models.CharField(max_length=30)

class DatabasePopulationAgent(models.Model): 
	pid = models.CharField(max_length=30)
	last_interaction = models.CharField(max_length=30)
	filenames = models.ManyToManyField(File)
	

