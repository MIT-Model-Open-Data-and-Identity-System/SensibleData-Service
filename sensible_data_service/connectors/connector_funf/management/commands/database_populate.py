from connectors.connector_funf.database_single_population import *
from sensible_auditor import audit

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			audit.Audit().d(type='connector_funf', tag='population', doc={'message': 'Running database population script'})
			load_files()
		except Exception as e:
			audit.Audit().e(type='connector_funf', tag='population', doc={'message': 'Exception thrown from database population script: ' + str(e)})
