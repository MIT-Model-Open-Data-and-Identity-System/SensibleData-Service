from connectors.connector_funf.database_single_population import *
import logging

from django.core.management.base import NoArgsCommand

log = logging.getLogger('sensible.' + __name__)

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			log.debug('population', extra ={'message': 'Running database population script'})
			load_files()
		except Exception as e:
			log.error('population', extra ={'message': 'Exception thrown from database population script: ' + str(e)})

