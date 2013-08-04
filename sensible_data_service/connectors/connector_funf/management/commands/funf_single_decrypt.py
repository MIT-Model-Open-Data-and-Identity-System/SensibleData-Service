from connectors.connector_funf.data_decryption import *
from utils.log import log

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
    	
    	if len(args) < 1:
    		log('Error','You have to give me the filename')
    		return;
    	#log('Debug','Will try to decrypt ' + args[0]);
    	try:
    		decrypt_file_from_upload(args[0]);
    	except Exception as e:
    		log.log('Error','Exception while single decrypting file ' + args[0] + ': ' + str(e))
