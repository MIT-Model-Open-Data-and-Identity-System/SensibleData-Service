import os.path
import shutil
import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import pdb;
from django.core.servers.basehttp import FileWrapper
import mimetypes
from utils import log
from django.conf import settings

from connectors.connector import connector
import bson.json_util as json

from connectors.connector_funf.models import ConnectorFunf

@csrf_exempt
def upload(request):
	log.log('Debug', 'Received POST')
	scope = 'all_probes'

	access_token = request.REQUEST.get('access_token', '')


	if request.META['CONTENT_TYPE'].split(';')[0]=='multipart/form-data':
#	if not request.META['CONTENT_TYPE']=='multipart/form-data;boundary=*****':
		try:
			uploaded_file = request.FILES['uploadedfile']
			if uploaded_file:
				try:
					
					#authorization = self.pipe.getAuthorization(access_token, scope=scope)
					authorization = ''
			
					if 'error' in authorization:
						upload_path = settings.CONNECTORS["connector_funf"]["config"]["upload_not_authorized_path"]
					else:
						upload_path = settings.CONNECTORS["connector_funf"]["config"]["upload_path"]

					if not os.path.exists(upload_path):
						os.mkdir(upload_path)
					
					filepath = os.path.join(upload_path, uploaded_file.name.split('.')[0].split('_')[0]+'_'+access_token+'_'+str(int(time.time()))+'.db')
					
					write_file(filepath, uploaded_file)

				except Exception as e:
					log.log('Error', 'Could not write: ' + str(e))
					return HttpResponse(status='500')
				else:
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
	pdb.set_trace();
	log.log('Debug', 'GET for config')
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
		mConnector = ConnectorFunf.objects.all()[0];
		pdb.set_trace();
		with open(mConnector.config_path) as config_file:
			
			print mConnector.config_path
			config = config_file.read()
	except IOError: pass
	return config

def chooseConfig(user):
	return "config.json"

