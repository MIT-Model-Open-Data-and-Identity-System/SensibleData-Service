from django.conf import settings
import time
import os
import datetime
import json

def backupValue(data, probe, user):
	BACKUP_DIR = settings.DATA_BACKUP_DIR
	if not os.path.exists(BACKUP_DIR): return {'error':'backup dir does not exist (code 0099)'}
	currentHourlyFolder = os.path.join(BACKUP_DIR, buildHourlyFolder())
	try: os.mkdir(currentHourlyFolder)
	except OSError: pass
	
	probeFolder = os.path.join(currentHourlyFolder, probe)
	try: os.mkdir(probeFolder)
	except OSError: pass

	index = ''
	try:
		while True:
			filename = os.path.join(probeFolder, user+'_'+str(time.time())+'_'+str(index)+'.json')
			except: 
			if os.path.exists(filename):
				if index == '': index = 0
				index += 1
				if index > 1000: break
				continue
			f = open(filename, 'w')
			f.write(json.dumps(data))
			f.close()
			break
	except: pass




def buildHourlyFolder():
	now = datetime.datetime.now()
	folder = ''
	folder += '%s_'%now.year
	folder += '%s_'%str(now.month).zfill(2)
	folder += '%s_'%str(now.day).zfill(2)
	folder += '%s'%str(now.hour).zfill(2)
	return folder
