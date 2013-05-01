import os
import datetime
import time
import shutil
from utils import log

def fail(filename, failed_directory_path, message):
	log.log('Error', message)
	safe_move(filename, failed_directory_path)

def safe_move(filename, move_to_path):
	try:
		shutil.move(filename, move_to_path)
	except:
		shutil.move(filename, os.path.join(move_to_path, str(time.time()) + '-' + os.path.basename(filename)))
