from utils.auth_database import AuthDatabase
from utils import service_config
from utils import SECURE_service_config

class AuthorizationManager(object):

	authDatabase = None

	def __init__(self):
		self.authDatabase = AuthDatabase()


	def getAuthorizationForToken(self, pipe, scope, token):
		authorizations = self.authDatabase.getDocuments({'service':service_config.SERVICE_NAME, 'pipe':pipe, 'scope': scope, 'params.token':token, 'valid':True}, pipe)
		try:
			authorization = authorizations[0]
		except IndexError: authorization = {'error':'no authorization found'}
		return authorization


	def insertAuthorization(self, user, pipe, scope, params):
		authorization = {'service':service_config.SERVICE_NAME, 'user':user, 'pipe':pipe, 'scope':scope, 'params':params, 'valid':True}
		return self.authDatabase.insert(authorization, pipe)
