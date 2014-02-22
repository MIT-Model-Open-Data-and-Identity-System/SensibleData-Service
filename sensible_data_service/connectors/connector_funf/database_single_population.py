from utils import database
import os
import fnmatch
import random
import time
from models import *
from utils import fail
import sqlite3
import shutil
import bson.json_util as json
import time
import hashlib
from anonymizer.anonymizer import Anonymizer
from collections import defaultdict
import sys, traceback
import authorization_manager.authorization_manager as authorization_manager
from django.conf import settings

import connectors.connectors_config

import traceback

import time
from accounts.models import UserRole
import logging

log = logging.getLogger('sensible.' + __name__)

myConnector = connectors.connectors_config.CONNECTORS['ConnectorFunf']['config']

db = database.Database()

valid_tokens = {};

def populate(documents_to_insert):
	inserted_counter = 0
	for probe in documents_to_insert:
		for role in documents_to_insert[probe]:
			population_start = time.time()	
			roles = role.split('@')

			inserted_counter += len(documents_to_insert[probe][role])
			try: db.insert(documents_to_insert[probe][role], probe, roles)
			except: pass

			log.debug('population_time', extra = {'ptime': '%.4f'%(time.time()-population_start), 'documents': inserted_counter, 'collection': probe, 'roles': role})
			inserted_counter = 0

def load_files(directory_to_load=myConnector['decrypted_path']):
	raw_filenames = [filename for filename in os.listdir(directory_to_load) if 	fnmatch.fnmatch(filename, '*.db')]
	
	failed_filenames = []
	
	jj = 0 
	documents_to_insert = defaultdict(lambda: defaultdict(list))
	for f in raw_filenames:
		#try:
		current_documents_to_insert, current_roles = load_file(f)
		if current_documents_to_insert == 0: 
			continue
		jj += 1
		for probe in current_documents_to_insert:
			documents_to_insert[probe]['@'.join(current_roles)] += current_documents_to_insert[probe]
		
		if jj == 20:
			jj = 0
			populate(documents_to_insert)
			documents_to_insert = defaultdict(lambda: defaultdict(list))
		#except: pass

	populate(documents_to_insert)

def load_file(filename):
	anonymizerObject = Anonymizer()
	
	documents_to_insert = defaultdict(list)
	#inserted_counter = 0
	proc_dir = os.path.join(myConnector['decrypted_path'], 'processing')
	if not os.path.exists(proc_dir):
		os.makedirs(proc_dir)
		
	decrypted_filepath = os.path.join(myConnector['decrypted_path'], filename)
	processing_filepath = os.path.join(proc_dir,filename)
	current_filepath = decrypted_filepath
	load_failed_path = myConnector['load_failed_path']
	roles = []

	if os.path.exists(decrypted_filepath) and not os.path.exists(processing_filepath):
		try:
			# move to processing
			moving_start = time.time()
			shutil.move(decrypted_filepath, proc_dir)
			
			current_filepath = processing_filepath
			# open connection to db file
			reading_start = time.time()
			conn = sqlite3.connect(processing_filepath)
			cursor = conn.cursor()
			
			# get the meta data from db file
			meta = {}
			(meta['device'], meta['uuid'], meta['device_id'], meta['sensible_token'], meta['device_bt_mac'], meta['timestamp']) = cursor.execute('select device, uuid, device_id, sensible_token, device_bt_mac, created from file_info').fetchone()
			
			meta['user'] = None
			try: 
				(user, token) = get_user_name(meta['sensible_token'], meta['device_id'], meta['timestamp'])
				meta['user'] = user.username
				meta['sensible_token'] = token
				roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
			except: pass


			if meta['user'] == None:
				if not os.path.exists(myConnector['decrypted_not_authorized']):
					os.makedirs(myConnector['decrypted_not_authorized'])
				shutil.move(current_filepath, myConnector['decrypted_not_authorized'])
				return (0,0)
			
			meta['device_id'] = anonymizerObject.anonymizeValue('device_id',meta['device_id'])
			
			# get the user associated with the token
			#meta['user'] = authorization_manager.getAuthorizationForToken(\
			#	'connector_funf.submit_data', meta['token']).user
			for row in cursor.execute('select * from data'):
				doc = row_to_doc(row, meta['user'], anonymizerObject )
				if doc == None:
					continue
				documents_to_insert[doc['probe']].append(dict(doc.items() + meta.items()))
			
			cursor.close();
#			for probe in documents_to_insert:
#				inserted_counter += len(documents_to_insert[probe])
#				try:
#					db.insert(documents_to_insert[probe], probe, roles)
#				except Exception as e:
#					pass
			os.remove(current_filepath);
			
		except Exception as e:
			log.error('population_error', extra = {'error':str(e)})
			if not 'already exists' in str(e):
				top = traceback.extract_stack()[-1]
				fail.fail(current_filepath, load_failed_path, 'Exception with file: ' + filename\
				+ '\n' + ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))
			else:
				pass
			
			return (0,0)
#	return inserted_counter
	return (documents_to_insert, roles)

def row_to_doc(row, user, anonymizerObject):
	random.seed(time.time())
	#TODO: separate this sanitization
	data_raw = row[3].replace('android.bluetooth.device.extra.DEVICE','android_bluetooth_device_extra_DEVICE')\
		.replace('android.bluetooth.device.extra.NAME', 'android_bluetooth_device_extra_NAME')\
		.replace('android.bluetooth.device.extra.CLASS', 'android_bluetooth_device_extra_CLASS')\
		.replace('android.bluetooth.device.extra.RSSI', 'android_bluetooth_device_extra_RSSI')
	data = []
	try:
		data = json.loads(data_raw)
		if data.has_key('PROBE'): #only get data from probes
			doc = {}
			doc['timestamp'] = int(row[2])
			doc['_id'] = hashlib.sha1(json.dumps(data)).hexdigest()+'_'+user+'_'+str(int(doc['timestamp']))
			doc['probe'] = data['PROBE'].replace('.','_')
			doc['data'] = anonymizerObject.anonymizeDocument(data, doc['probe'])
			doc['name'] = row[1]
			doc['timestamp_added'] = int(time.time())
			return doc
		else:
			return None
	except Exception as e:
		log.error('population_error', extra = {'error': str(e), 'data': data})
		return None
		
		
# returns the user associated with the token, or None, if the token is not valid
def get_user_name(token, device_id, timestamp):
	#workaround for missing token in the file
	if len(token) == 0:
		authorization = authorization_manager.getAuthorizationForDevice('connector_funf.submit_data', device_id, timestamp)
		if (authorization == None): return (None, None)
		return (authorization.user, authorization.access_token.token)

	if token in valid_tokens.keys():
		return valid_tokens[token]
	authorization = authorization_manager.getAuthorizationForToken('connector_funf.submit_data', token)
	if (authorization == None):
		return (None, None)
	else:
		valid_tokens[token] = (authorization.user, token)
		return (authorization.user, token)
