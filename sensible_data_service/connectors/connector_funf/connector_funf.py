import os.path
import shutil
import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from backup import backup
import pdb;
from django.core.servers.basehttp import FileWrapper
import mimetypes
from utils import log
from django.conf import settings

from connectors.connector import connector
import bson.json_util as json

#from connectors.connector_funf.models import ConnectorFunf
import connectors.connectors_config;
import authorization_manager

from subprocess import Popen, PIPE

# bug fix
# see http://stackoverflow.com/questions/13193278/understand-python-threading-bug
# import threading
# threading._DummyThread._Thread__stop = lambda x: 42
# end of bug fix


import random
import re

myConnector = connectors.connectors_config.CONNECTORS['ConnectorFunf']['config']

@csrf_exempt
def rescue(request):
	log.log('Debug','Rescue ' + request.POST['imei'] + ' @ ' + request.POST['lat'] + ',' + request.POST['lon'] + ' ~' + request.POST['acc'] + ' on ' + request.POST['timestamp'] + ' from ' + request.POST['provider'] + ' due to ' + request.POST['action'])
	return HttpResponse('got it','text/javascript', status=200)

@csrf_exempt
def upload(request):
	random.seed(time.time())
	log.log('Debug', 'Received POST')
	scope = 'all_probes'



	if request.META['CONTENT_TYPE'].split(';')[0]=='multipart/form-data':
		try:
			uploaded_file = request.FILES['uploadedfile']
			if uploaded_file:
				#try:
					
					#authorization = authorization_manager.getAuthorizationForToken(scope, access_token)
					#mConnector = ConnectorFunf.objects.all()[0];
					#if ('error' in authorization) or (authorization == None):
					#	upload_path = mConnector.upload_not_authorized_path;
					#else:
					#	upload_path = mConnector.upload_path
					upload_path = myConnector['upload_path']	
					backup_path = myConnector['backup_path']

					if not os.path.exists(upload_path):
						os.makedirs(upload_path)
					if not os.path.exists(backup_path):
						os.makedirs(backup_path)
					
					filename = uploaded_file.name.split('.')[0].split('_')[0]+'_'+str(int(time.time()*1000))+'.db'
					filepath = os.path.join(upload_path, filename)
					while os.path.exists(filepath):
						parts = filename.split('.db');
						counted_parts = re.split('__',parts[0]);
						appendix = str(int(random.random()*10000))
						filename = counted_parts[0] + '__' + appendix + '.db'
						filepath = os.path.join(upload_path, filename)

					write_file(filepath, uploaded_file)
					backup.backupFile(filepath, "connector_funf")
					#shutil.copy(filepath, os.path.join(backup_path, filename))
					
					# run decryption in the background
					#log.log('Debug', settings.ROOT_DIR + './manage.py funf_single_decrypt' + filename)
					#p = Popen([settings.ROOT_DIR + './manage.py','funf_single_decrypt',filename], stdout=PIPE, stderr=PIPE)

				#except Exception as e:
				#	log.log('Error', 'Could not write: ' + str(e))
				#	return HttpResponse(status='500')
				#else:
					return HttpResponse(json.dumps({'ok':'success'}))
			else:
				log.log('Error', 'failed to read')
		except KeyError as e:
			log.log('Error', 'Key error: ' + str(e))
			pass
	# bad request
	return HttpResponse(status='500')

def write_file(filepath, file):
	with open(filepath, 'wb') as output_file:
		while True:
			chunk = file.read(1024)
			if not chunk:
				break
			output_file.write(chunk)


def config(request):
	#pdb.set_trace();
	#log.log('Debug', 'GET for config')
	access_token = request.REQUEST.get('access_token', '')
	#authorization = self.pipe.getAuthorization(access_token)
	#config = self.readConfig(authorization['user'])
	config = readConfig('dummy')
	if config:
		return HttpResponse(config)
	else:
		return HttpResponse(status='500')

def readConfig(user):
	config = None
	try:
		with open(myConnector['config_path']) as config_file:
			config = config_file.read()
	except IOError: pass
	return config

def chooseConfig(user):
	return "config.json"

