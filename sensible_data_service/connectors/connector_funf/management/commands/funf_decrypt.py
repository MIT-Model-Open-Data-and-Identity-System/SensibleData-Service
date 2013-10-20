from connectors.connector_funf.data_decryption import *
from sensible_audit import audit

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			audit.Audit().d(type='connector_funf', tag='decryption', doc={'message': 'Running FUNF decryption script'})
			decrypt()
		except Exception as e:
			audit.Audit().e(type='connector_funf', tag='decryption', doc={'message': 'Exception thrown from FUNF decryption script: ' + str(e)})
