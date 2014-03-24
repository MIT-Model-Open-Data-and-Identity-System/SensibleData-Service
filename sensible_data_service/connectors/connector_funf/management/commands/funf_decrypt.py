from connectors.connector_funf.data_decryption import *
from django.core.management.base import NoArgsCommand
from sensible_audit import audit

log = audit.getLogger(__name__)

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			log.debug({'message': 'Running FUNF decryption script'})
			decrypt()
		except Exception as e:
			log.debug({'message': 'Exception thrown from FUNF decryption script: ' + str(e)})
