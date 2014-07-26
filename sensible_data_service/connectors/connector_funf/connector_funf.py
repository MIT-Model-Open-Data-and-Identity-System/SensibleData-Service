import os.path
import shutil
import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from backup import backup
from django.core.servers.basehttp import FileWrapper
import mimetypes
from django.conf import settings
from sensible_audit import audit

log = audit.getLogger(__name__)

from connectors.connector import connector
import bson.json_util as json

import connectors.connectors_config
import authorization_manager

from subprocess import Popen, PIPE
from django.shortcuts import redirect

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
	log.error({'tag': 'call_home', 'message': 'Rescue ' + request.POST['imei'] + ' @ ' + request.POST['lat'] + ',' + request.POST['lon'] + ' ~' + request.POST['acc'] + ' on ' + request.POST['timestamp'] + ' from ' + request.POST['provider'] + ' due to ' + request.POST['action']})
	return HttpResponse('got it','text/javascript', status=200)

@csrf_exempt
def upload(request):
	random.seed(time.time())
	log.debug({'tag': 'post', 'message': 'Received POST'})
	scope = 'all_probes'



	if request.META['CONTENT_TYPE'].split(';')[0]=='multipart/form-data':
		try:
			uploaded_file = request.FILES['uploadedfile']
			if uploaded_file:
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
					
					return HttpResponse(json.dumps({'ok':'success'}))
			else:
				log.error({'tag': 'upload_fail'})
		except KeyError as e:
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
	access_token = request.REQUEST.get('access_token', None)
	bearer_token = request.REQUEST.get('bearer_token', None)

	if not bearer_token and access_token:
		current_url = request.build_absolute_uri()
		url = current_url.replace('access_token', 'bearer_token')
		return redirect(url) 

	try: user = authorization_manager.authorization_manager.authenticate_token(request)['user']
	except: user = None
	config = readConfig(user)
	if config:
		return HttpResponse(config)
	else:
		return HttpResponse(status='500')

def readConfig(user):
	config = None
	try:
		with open(myConnector['config_path']+'_'+user.username) as config_file: config = config_file.read()
	except:
		try:
			with open(myConnector['config_path']) as config_file: config = config_file.read()
		except: pass
	return config
