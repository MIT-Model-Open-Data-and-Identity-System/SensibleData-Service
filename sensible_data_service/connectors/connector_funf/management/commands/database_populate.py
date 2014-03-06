from connectors.connector_funf.database_single_population import *
from django.core.management.base import NoArgsCommand
from sensible_audit import audit

log = audit.getLogger(__name__)

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			log.debug({'message': 'Running database population script'})
			load_files()
		except Exception as e:
			log.error({'message': 'Exception thrown from database population script: ' + str(e)})

