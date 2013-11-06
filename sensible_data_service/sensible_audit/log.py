import os
import datetime
import time
import shutil
from django.conf import settings

def log(tag, text):
	filename = os.path.join(settings.DATA_LOG_DIR, 'log_' + str(datetime.date.today()) + '.txt')
	if not os.path.exists(settings.DATA_LOG_DIR):
		os.makedirs(settings.DATA_LOG_DIR)
		
	if not os.path.exists(filename):
		f = open(filename, 'w')
		os.chmod(f.name, 0660)
	else:
		f = open(filename, 'a')
	f.write('[' + str(datetime.datetime.now()) + ']' + '[' + tag + '] ' + text + '\n')
	f.close()
	del f
