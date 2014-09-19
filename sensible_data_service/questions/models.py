from django.db import models

class QualityPrizeWinners(models.Model):
	user = models.CharField(max_length=100, blank=True)
	start_timestamp = models.DateTimeField(blank=True)
	end_timestamp = models.DateTimeField(blank=True)
	quality = models.FloatField(blank=True)
	prize = PrizeTicket(blank=True, unique=True)
	claimed = models.BooleanField(default=False)

class PrizeTicket(models.Model):
	code = models.CharField