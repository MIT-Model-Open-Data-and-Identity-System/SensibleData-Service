from connectors.connector_funf.data_decryption import *
from sensible_audit import audit

log = audit.getLogger(__name__)

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
    	
    	if len(args) < 1:
		log.error({'message': 'You have to give me the filename'})
    		return;
    	#log('Debug','Will try to decrypt ' + args[0]);
    	try:
    		decrypt_file_from_upload(args[0]);
    	except Exception as e:
		log.error({'message': 'Exception while single decrypting file ' + args[0] + ': ' + str(e)})


