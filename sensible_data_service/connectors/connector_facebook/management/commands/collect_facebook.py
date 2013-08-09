from django.core.management.base import NoArgsCommand
from connectors.connector_facebook.connector_facebook import *

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		collect_facebook()
