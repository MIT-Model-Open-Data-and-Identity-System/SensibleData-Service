from connectors.connector_funf import data_re_decryption
from django.core.management.base import NoArgsCommand
from sensible_audit import audit

log = audit.getLogger(__name__)

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			log.debug({'message': 'Running FUNF decryption failed script'})
			data_re_decryption.decrypt_directory()
		except Exception as e:
			log.debug({'message': 'Exception thrown from FUNF decryption failed script: ' + str(e)})
