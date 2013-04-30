import os.path
import shutil
import datetime
import time
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from django.core.servers.basehttp import FileWrapper
import mimetypes
from utils import service_config
from utils import SECURE_service_config
from utils import log

from connector_pipes.connector_pipe_funf import connector_pipe_funf
from connectors.connector import connector
		

class ConnectorFunf(connector.Connector):

	pipe = None


	def __init__(self): 
		super(ConnectorFunf, self).__init__()
		self.pipe = connector_pipe_funf.ConnectorFunfPipe()

	def upload(self, request):
		log.log('Debug', 'Received POST')

		access_token = request.REQUEST.get('access_token', '')


		if request.META['CONTENT_TYPE'].split(';')[0]=='multipart/form-data':
	#	if not request.META['CONTENT_TYPE']=='multipart/form-data;boundary=*****':
			try:
				uploaded_file = request.FILES['uploadedfile']
				if uploaded_file:
					try:
						
						user = self.pipe.getUser(access_token)
				
						if user == '':
							upload_path = service_config.FUNF["upload_not_authorized_path"]
						else:
							upload_path = service_config.FUNF["upload_path"]

						if not os.path.exists(upload_path):
							os.mkdir(upload_path)
						
						filepath = os.path.join(upload_path, uploaded_file.name)
						
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
		return HttpResponse('here')

	def write_file(self, filepath, file):
		with open(filepath, 'wb') as output_file:
			while True:
				chunk = file.read(1024)
				if not chunk:
					break
				output_file.write(chunk)


	def config(self, request):
		pass


@csrf_exempt
def upload(request):
	connectorFunf = ConnectorFunf()
	return connectorFunf.upload(request)



	
def config(request):
	connectorFunf = ConnectorFunf()
	return connectorFunf.config(request)
