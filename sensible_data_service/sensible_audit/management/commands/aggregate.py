from django.conf import settings
from django.core.management.base import BaseCommand

from sensible_audit.management.commands.agg_utils import *
from sensible_audit.management.commands.aggregator import *

class Command(BaseCommand):

	args = '<level> DATE'

	def handle(self, *args, **options):
		# time aggregation levels
		levels = ['day', 'week']

		if len(args) < 2:
			self.stderr.write('Error: Number of arguments not valid.')
			return

		level = args[0]
		date = date_is_valid(level, args[1])

		if not level in levels or not date: return
		
		self.stdout.write('Aggregating for %s on %s' % (level, date))

		if level == 'day':
			aggregate_day_user(date)
			aggregate_day_researcher(date)
			aggregate_stats(date)
		else:
			aggregate_week_user(date)
			aggregate_week_researcher(date)
			aggregate_stats_week(date)