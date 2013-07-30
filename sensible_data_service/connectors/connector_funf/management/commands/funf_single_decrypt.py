from connectors.connector_funf.data_decryption import *
from utils.log import log

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
    	
    	if len(args) < 1:
    		print 'You must supply the name of the file'
    		return;
    	try:
    		decrypt_file(args[0]);
    	except Exception as e:
    		log('Error','Exception while single decrypting file ' + args[0] + ': ' + str(e))
