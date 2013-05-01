from connectors.connector_funf.database_population import *
from utils.log import log

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			log('Debug', 'Running FUNF decryption script')
			populate()
		except Exception as e:
			log('Error', 'Exception thrown from FUNF decryption script: ' + str(e))
