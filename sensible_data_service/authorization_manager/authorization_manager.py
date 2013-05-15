from utils.auth_database import AuthDatabase
from utils import service_config
from utils import SECURE_service_config
from application_manager import application_manager
from django.http import HttpResponse
from bson import json_util as json
import uuid
import time
from identity_manager import identity_manager
from platform_manager import platform_manager

class AuthorizationManager(object):

	authDatabase = None
	applicationManager = None
	identityManager = None

	def __init__(self):
		self.authDatabase = AuthDatabase()
		self.applicationManager = application_manager.ApplicationManager()
		self.identityManager = identity_manager.IdentityManager()


	def getAuthorizationForToken(self, connector, scope, token):
		authorizations = self.authDatabase.getDocuments({'service': service_config.SERVICE_NAME, 'connector': connector, 'scope': scope, 'params.token':token, 'valid':True}, connector)
		try:
			authorization = authorizations[0]
		except IndexError: authorization = {'error':'no authorization found'}
		return authorization


	def insertAuthorization(self, user, connector, scope, client_id, params):
		authorization = {'service': service_config.SERVICE_NAME, 'user': user, 'connector': connector, 'scope':scope, 'client_id': client_id, 'params': params, 'valid': True}
		return self.authDatabase.insert(authorization, connector)

	def insertAuthorizationCode(self, authorization_code, connector):
		return self.authDatabase.insert(authorization_code, connector+'_'+'authorization_code')


	def generateOAuthAuthorizationCode(self, user, connector, scopes, client_id):
		#TODO: add introspection to the token
		authorization_code = str(uuid.uuid4()).replace('-','')

		authorization_code_object = {}
		authorization_code_object['user'] = user
		authorization_code_object['connector'] = connector
		authorization_code_object['scopes'] = scopes
		authorization_code_object['client_id'] = client_id
		authorization_code_object['authorization_code'] = authorization_code
		authorization_code_object['generated_timestamp'] = time.time()
		authorization_code_object['valid_for'] = 300
		authorization_code_object['valid'] = True
		self.insertAuthorizationCode(authorization_code_object, connector)
		return authorization_code
		
	def getClient(self, client_id):
		client = self.authDatabase.getDocuments({'params.client_id': client_id}, 'application')[0]
		return client

def connectorFunf(request):
	
	platformManager = platform_manager.PlatformManager()
	if not platformManager.validateRequest(request):
		response = {'error': 'request not valid'}
		return HttpResponse(json.dumps(response))



	user_ticket = request.REQUEST.get('user_ticket', '')


	authorizationManager = AuthorizationManager()
	user = authorizationManager.identityManager.requestUserForTicket(user_ticket)

	scopes = request.REQUEST.get('scope', '')
	client_id = request.REQUEST.get('client_id', '')
	if user_ticket == '':
		response = {'error':'no user ticekt provided'}
		return HttpResponse(json.dumps(response))
	if user == '':
		response = {'error':'user unknown'}
		return HttpResponse(json.dumps(response))
	if scopes == '':
		response = {'error':'no scope provided'}
		return HttpResponse(json.dumps(response))
	if client_id == '':
		response = {'error': 'no client_id provided'}
		return HttpResponse(json.dumps(response))

	client = authorizationManager.getClient(client_id)
	
	scopes = scopes.split(',')
	valid_scopes = []
	for scope in scopes:
		if scope in client['scopes']:
			valid_scopes.append(scope)
		
	authorization_code = authorizationManager.generateOAuthAuthorizationCode(user, 'connector_funf', valid_scopes, client_id)
		
	#TODO: redirect to registered redirect url for application
	response = {'ok':'authorization created', 'authorization_code': authorization_code}
	return HttpResponse(json.dumps(response))
