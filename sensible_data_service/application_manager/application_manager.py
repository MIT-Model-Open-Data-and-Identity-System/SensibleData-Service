from utils.auth_database import AuthDatabase
from utils import service_config
from utils import SECURE_service_config
import uuid
from django.http import HttpResponse
import bson.json_util as json

class ApplicationManager(object):
	
	authDatabase = None

	def __init__(self):
		self.authDatabase = AuthDatabase()

	def registerApplication(self, name, owner, connector, scopes, description, params, connector_type):
		application = dict()
		application['name'] = name
		application['id'] = str(uuid.uuid4())
		application['service'] = service_config.SERVICE_NAME
		application['owner'] = owner
		application['connector'] = connector
		application['scopes'] = scopes.split(',')
		application['params'] = json.loads(params)
		application['description'] = description
		application['connector_type'] = connector_type

		validation = self.validateApplication(application)


		if 'error' in validation:			
			return validation

			
		application['required_pipes'] = []
		for scope in application['scopes']:
			if self.isPipeRequired(application): application['required_pipes'].append(scope)
		

		self.authDatabase.insert(application, 'application')


		return application

	def validateApplication(self, application):
		#TODO: we need simple rule-based mechanism for allowing applications
		validation = {}
		if not application['name']: 
			validation['error'] = 'wrong name'
			return validation
		if not application['owner'] == 'hopbeatdev19gmailcom':
			validation['error'] = 'user not authorized'
			return validation
		if not application['connector'] in service_config.CONNECTORS:
			validation['error'] = 'invalid connector'
			return validation
		if not application['connector_type'] == service_config.CONNECTORS[application['connector']]['config']['connector_type']:
			validation['error'] = 'invalid connector type'
			return validation
		for scope in application['scopes']:
			if not scope in service_config.CONNECTORS[application['connector']]['scopes']: 	
				validation['error'] = 'invalid scope'
				return validation
		if self.authDatabase.getDocuments({'name':application['name']}, 'application').count():
			validation['error'] = 'application name already exists'
			return validation
		if self.authDatabase.getDocuments({'params':application['params']}, 'application').count():
			validation['error'] = 'application with those parameters already exists'
			return validation
			
			
			
		return validation


	def isPipeRequired(self, application):
		#TODO: simple rule based mechansism for determining whether we want the pipes to be required
		return True


	def registerResourceApplication(self, name, owner, connector, scopes, description, params):
		return self.registerApplication(name, owner, connector, scopes, description, params, connector_type='client')


def registerResourceApp(request):
	name = request.REQUEST.get('name', '')
	#TODO: owner comes from authentication
	owner = request.REQUEST.get('owner', '')
	connector = request.REQUEST.get('connector', '')
	scopes = request.REQUEST.get('scopes', '')
	description = request.REQUEST.get('description', '')
	params = request.REQUEST.get('params', '')

	applicationManager = ApplicationManager()
	response = applicationManager.registerResourceApplication(name, owner, connector, scopes, description, params)
	return HttpResponse(json.dumps(response))
