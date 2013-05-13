import os.path
import shutil
import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from django.core.servers.basehttp import FileWrapper
import mimetypes
from utils import service_config
from utils import SECURE_service_config
from utils import log

from connector_pipes.connector_pipe_funf import connector_pipe_funf
from connectors.connector import connector
import bson.json_util as json

class ConnectorFunf(connector.Connector):

	pipe = None


	def __init__(self): 
		super(ConnectorFunf, self).__init__()
		self.pipe = connector_pipe_funf.ConnectorFunfPipe()

	def upload(self, request):
		log.log('Debug', 'Received POST')
		scope = 'all_probes'

		access_token = request.REQUEST.get('access_token', '')


		if request.META['CONTENT_TYPE'].split(';')[0]=='multipart/form-data':
	#	if not request.META['CONTENT_TYPE']=='multipart/form-data;boundary=*****':
			try:
				uploaded_file = request.FILES['uploadedfile']
				if uploaded_file:
					try:
						
						authorization = self.pipe.getAuthorization(access_token, scope=scope)
				
						if 'error' in authorization:
							upload_path = service_config.CONNECTORS["connector_funf"]["config"]["upload_not_authorized_path"]
						else:
							upload_path = service_config.CONNECTORS["connector_funf"]["config"]["upload_path"]

						if not os.path.exists(upload_path):
							os.mkdir(upload_path)
						
						filepath = os.path.join(upload_path, uploaded_file.name.split('.')[0].split('_')[0]+'_'+access_token+'_'+str(int(time.time()))+'.db')
						
						self.write_file(filepath, uploaded_file)

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

	def write_file(self, filepath, file):
		with open(filepath, 'wb') as output_file:
			while True:
				chunk = file.read(1024)
				if not chunk:
					break
				output_file.write(chunk)


	def config(self, request):
		log.log('Debug', 'GET for config')
		access_token = request.REQUEST.get('access_token', '')
		authorization = self.pipe.getAuthorization(access_token)
		config = self.readConfig(authorization['user'])
		if config:
			return HttpResponse(config)
	        else:
        		return HttpResponse(status='500')

	def readConfig(self, user):
		config = None
		try:
			with open(service_config.CONNECTORS["connector_funf"]["config"]["config_path"]+self.chooseConfig(user)) as config_file:
				config = config_file.read()
		except IOError: pass
		return config

	def chooseConfig(self, user):
		return "config.json"

@csrf_exempt
def upload(request):
	connectorFunf = ConnectorFunf()
	return connectorFunf.upload(request)



	
def config(request):
	connectorFunf = ConnectorFunf()
	return connectorFunf.config(request)
