from connectors.connector_funf.data_decryption import *
import logging

from django.core.management.base import NoArgsCommand

log = logging.getLogger('sensible.' + __name__)

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			log.debug('decryption', extra={'message': 'Running FUNF decryption script'})
			decrypt()
		except Exception as e:
			log.debug('decryption', extra={'message': 'Exception thrown from FUNF decryption script: ' + str(e)})
