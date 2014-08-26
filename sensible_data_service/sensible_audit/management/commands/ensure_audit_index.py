from django.conf import settings
from django.core.management.base import BaseCommand

from sensible_audit.management.commands.aggregator import *

class Command(BaseCommand):

	def handle(self, *args, **options):
		ensure_indexes()