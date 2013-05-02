from utils import database
import os
import fnmatch

from models import *
from utils import service_config
from utils import fail
from utils import log
import sqlite3
import shutil
import bson.json_util as json
import time
import hashlib

#TODO: add turn on in config

def populate():
	pid = os.getpid()
	touchCreationLock()
	db = database.Database()
	if not start(pid):
		removeCreationLock()
		return

	run(db)
	end(pid)

def touchCreationLock():
#TODO: create file
	pass

def removeCreationLock():
#TODO: remove file
	pass


def start(pid):
	active_processes = checkActiveProcesses()
	print active_processes
	if active_processes >= service_config.CONNECTORS['connector_funf']['config']['max_population_processes']:
		return False
	DatabasePopulationAgent.objects.create(pid=str(pid))
	return True

def run(db):
	print 'running'
	decrypted_path = service_config.CONNECTORS['connector_funf']['config']['decrypted_path']
	load_failed_path = service_config.CONNECTORS['connector_funf']['config']['load_failed_path']
	raw_filenames = [filename for filename in os.listdir(decrypted_path) if fnmatch.fnmatch(filename, '*.db')]


	raw_filenames = raw_filenames[:service_config.CONNECTORS['connector_funf']['config']['max_population_files']]
	filenames = [os.path.join(decrypted_path, filename) for filename in raw_filenames]

	print raw_filenames
	proc_dir = os.path.join(decrypted_path, 'processing')
	failed_filenames = []

	for f in filenames:	
		try:
			shutil.move(f, proc_dir)
		except Exception as e:
			log.log('Debug', 'File: ' + str(f) + ' already exists.')
			#TODO: remove files that already exist
			failed_filenames.append(os.path.basename(f))

	raw_filenames = [e for e in raw_filenames if e not in failed_filenames]
	filenames = [os.path.join(proc_dir, filename) for filename in raw_filenames]

	cursor = None
	documents_to_insert = []
	filenames_to_remove = []
	nof_files = len(filenames)
	file_count = 0
	
	for filename in filenames:
		file_count += 1
		if not os.path.exists(filename):
			continue
		log.log('Debug', 'Populating to DB, file(%d/%d): %s' % (file_count, nof_files, filename))
		try:
			conn = sqlite3.connect(filename)
			cursor = conn.cursor()
		except Exception as e:
			fail.fail(filename, load_failed_path, 'Exception thrown:' + str(e) + '. While trying to open sqlite file: ' + filename)
			continue


		try:
			device = cursor.execute('select device from file_info').fetchone()[0]
			uuid = cursor.execute('select uuid from file_info').fetchone()[0]
			device_id = ''
			try:
				device_id = cursor.execute('select device_id from file_info').fetchone()[0]
			except Exception as e:
				fail.fail(filename, load_failed_path, 'Exception thrown: ' + str(e) + '. While trying to extract device_id from file: ' + filename)
				continue

			#TODO: get user from token
			user = 'todo_user'
			if not user:
				log.log('Debug', 'User does not exist for device id: ' + str(device_id))
				fail.fail(filename, load_failed_path, 'No user found in database. Device id: ' + str(device_id))
				continue
	
			for row in cursor.execute('select * from data'):
				name = row[1]
				timestamp = row[2]
				data = json.loads(row[3])
				#TODO: encrypt data
				doc = {}
				#TODO: graceful handling duplicates
				doc['_id'] = hashlib.sha1(json.dumps(data)).hexdigest()+'_'+user
				doc['uuid'] = uuid
				doc['device'] = device
				doc['device_id'] = device_id
				doc['user'] = user
				doc['data'] = data
				doc['name'] = name
				doc['timestamp'] = float(timestamp)
				doc['timestamp_added'] = time.time()
				#TODO: extra fields
				documents_to_insert.append(doc)
	
		except Exception as e:
			fail.fail(filename, load_failed_path, 'Exception thrown: ' + str(e) + '. While extracting data from file: ' + filename)
			continue
	
		cursor.close()
		log.log('Debug', 'Adding file to be populated')
		filenames_to_remove.append(filename)
	

	#TODO: make sure that the duplicates logic works
	#TODO: split documents into collections
	db.insert(documents_to_insert, 'data')
	for filename in filenames_to_remove:
		os.remove(filename)


def checkIfProcessAlive(pid):
	try:
		os.kill(int(pid), 0)
		return True
	except:
		return False

def removeProcess(pid):
	ps = DatabasePopulationAgent.objects.filter(pid=pid)
	for p in ps:
		p.delete()

def checkActiveProcesses():
	processes = DatabasePopulationAgent.objects.filter()
	for process in processes:
		if not checkIfProcessAlive(process.pid): removeProcess(process.pid)
		#TODO: check if process is timeout
	
	processes = DatabasePopulationAgent.objects.filter()
	return processes.count()


def end(pid):
	removeProcess(pid)
