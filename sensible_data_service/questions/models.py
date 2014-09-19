from django.db import models

class PrizeTicket(models.Model):
	code = models.CharField(max_length=100, unique=True)

class QualityPrizeWinners(models.Model):
	user = models.CharField(max_length=100, blank=True)
	start_timestamp = models.DateTimeField(blank=True)
	end_timestamp = models.DateTimeField(blank=True)
	quality = models.FloatField(blank=True)
	prize = models.OneToOneField(PrizeTicket)
	claimed = models.BooleanField(default=False)