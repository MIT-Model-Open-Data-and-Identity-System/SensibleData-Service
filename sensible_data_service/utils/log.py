from utils import service_config
import os
import datetime
import time
import shutil

def log(tag, text):
	filename = os.path.join(service_config.LOG_FILE_PATH, 'log_' + str(datetime.date.today()) + '.txt')
	if not os.path.exists(filename):
		f = open(filename, 'w')
		os.chmod(f.name, 0660)
	else:
		f = open(filename, 'a')
	f.write('[' + str(datetime.datetime.now()) + ']' + '[' + tag + '] ' + text + '\n')
	f.close()
	del f
