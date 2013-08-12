from utils import database
import os
import fnmatch
import random
import time
from models import *
from utils import fail
from utils import log
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
import pdb

import time

myConnector = connectors.connectors_config.CONNECTORS['ConnectorFunf']['config']

db = database.Database()

valid_tokens = {};

def load_files(directory_to_load=myConnector['decrypted_path']):
	raw_filenames = [filename for filename in os.listdir(directory_to_load) if 	fnmatch.fnmatch(filename, '*.db')]
	
	failed_filenames = []
	
	for f in raw_filenames:
		population_start = time.time()	
		load_file(f)
		log.log('Debug','Population time: ' + str(time.time()-population_start) + ' ms')
		

def load_file(filename):
	#pdb.set_trace()
	#log.log('Debug', 'Trying to populate db with ' + filename);
	#connection_time = time.time()
	#log.log('Debug', 'Connection to db: ' + str(time.time() - connection_time) + ' s');
	anonymizerObject = Anonymizer()
	
	documents_to_insert = defaultdict(list)
	
	proc_dir = os.path.join(myConnector['decrypted_path'], 'processing')
	if not os.path.exists(proc_dir):
		os.makedirs(proc_dir)
		
	decrypted_filepath = os.path.join(myConnector['decrypted_path'], filename)
	processing_filepath = os.path.join(proc_dir,filename)
	current_filepath = decrypted_filepath
	load_failed_path = myConnector['load_failed_path']

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
			(meta['device'], meta['uuid'], meta['device_id'], meta['sensible_token'], meta['device_bt_mac']) = \
				cursor.execute('select device, uuid, device_id, sensible_token, device_bt_mac from file_info').fetchone()
			
			meta['user'] = get_user_name(meta['sensible_token'])
			if meta['user'] == None:
				if not os.path.exists(myConnector['decrypted_not_authorized']):
					os.makedirs(myConnector['decrypted_not_authorized'])
				shutil.move(current_filepath, myConnector['decrypted_not_authorized'])
				return 
			
			meta['device_id'] = anonymizerObject.anonymizeValue('device_id',meta['device_id'])
			
			#pdb.set_trace()
			# get the user associated with the token
			#meta['user'] = authorization_manager.getAuthorizationForToken(\
			#	'connector_funf.submit_data', meta['token']).user
			for row in cursor.execute('select * from data'):
				doc = row_to_doc(row, meta['user'], anonymizerObject )
				if doc == None:
					continue
				documents_to_insert[doc['probe']].append(dict(doc.items() + meta.items()))
			
			cursor.close();
			#pdb.set_trace()
			#log.log('Debug','DB reading time: ' + str(time.time() - reading_start) + ' s')
			upload_start = time.time()
			for probe in documents_to_insert:
				db.insert(documents_to_insert[probe], probe)
			#log.log('Debug','DB upload time: ' + str(time.time() - upload_start) + ' s')	
			os.remove(current_filepath);
			
		except Exception as e:
			log.log('Error', str(e));
			if not 'already exists' in str(e):
				top = traceback.extract_stack()[-1]
				fail.fail(current_filepath, load_failed_path, 'Exception with file: ' + filename\
				+ '\n' + ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])]))
			else:
				pass
			
			return False

def row_to_doc(row, user, anonymizerObject):
	#pdb.set_trace()
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
			doc['timestamp'] = float(row[2])
			doc['_id'] = hashlib.sha1(json.dumps(data)).hexdigest()+'_'+user+'_'+str(int(doc['timestamp']))+'_'+str(random.random())+'_'+str(random.random())
			doc['probe'] = data['PROBE'].replace('.','_')
			doc['data'] = anonymizerObject.anonymizeDocument(data, doc['probe'])
			doc['name'] = row[1]
			doc['timestamp_added'] = time.time()
			return doc
		else:
			return None
	except Exception as e:
		log.log('ERROR',str(e) + ' in ' + json.dumps(data))
		return None
		
		
# returns the username associated with the token, or None, if the token is not valid
def get_user_name(token):
	# debug
	return 'DEBUG_USER'
	if len(token) == 0:
		return None
	if token in valid_tokens.keys():
		return valid_tokens[token]
	authorization = authorization_manager.getAuthorizationForToken('connector_funf.submit_data', token)
	if (authorization == None):
		return None
	else:
		valid_tokens[token] = authorization.user.username
		return authorization.user.username
			
			
			
