import sys
import os
import shutil
import fnmatch
from dbdecrypt import decrypt_if_not_db_file
from decrypt import key_from_password
from utils import SECURE_settings
from utils import log, fail
from django.conf import settings
from connectors.connector_funf.models import ConnectorFunf 

#import pdb

mConnector = ConnectorFunf.objects.all()[0];

key = key_from_password(SECURE_settings.CONNECTORS['connector_funf']['db_pass']);

def decrypt():
	decrypt_directory()

def decrypt_directory(directory_to_decrypt=mConnector.upload_path):
	decrypted_directory_path = mConnector.decrypted_path
	decryption_failed_path = mConnector.decryption_failed_path;
	backup_path = mConnector.backup_path;
	#TODO
	raw_filenames = [filename for filename in os.listdir(directory_to_decrypt) if fnmatch.fnmatch(filename, '*.db')]
	#raw_filenames = [filename for filename in os.listdir(directory_to_decrypt) if fnmatch.fnmatch(filename, '*.orig')]
	filenames = [os.path.join(directory_to_decrypt, filename) for filename in raw_filenames]
	proc_dir = os.path.join(directory_to_decrypt, 'processing')
	if not os.path.exists(proc_dir):
		os.mkdir(proc_dir)
	failed_filenames = []
	
	for f in filenames:
		try:
			shutil.move(f, proc_dir)
		except Exception as e:
			fail.fail(f, decryption_failed_path, 'Exception thrown: ' + str(e) + '. While moving file: ' + f)
			failed_filenames.append(os.path.basename(f))

	raw_filenames = [e for e in raw_filenames if e not in failed_filenames]
	filenames = [os.path.join(proc_dir, filename) for filename in raw_filenames]


	for filename in filenames:
		try:
			# If successfull we move the decrypted file to the decrypted directory
			#pdb.set_trace();
			if decrypt_if_not_db_file(filename, key, extension=None):
				fail.safe_move(filename, decrypted_directory_path)
				
				# Move original db file to original directory if it exists -- if db file is already decrypted .orig will not exist
				orig_filename = filename + '.orig'
				#orig_filename = filename
				#pdb.set_trace()
				if os.path.exists(orig_filename):
					os.remove(orig_filename)

			# If decryption fails we move the file to the failed directory
			else:
				fail.fail(filename, decryption_failed_path, 'Could not decrypt file: ' + filename)
		except Exception as e:
			# If anything goes wrong we move the file to the failed directory
			fail.fail(filename, decryption_failed_path, 'Exception thrown: ' + str(e) + '. While decrypting file: ' + filename)


if __name__ == '__main__':
	if len(sys.argv) == 2:
		directory = sys.argv[1]
		decrypt_directory(directory_to_decrypt=directory)
	else:
		decrypt_directory()
