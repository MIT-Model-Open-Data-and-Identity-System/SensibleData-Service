from .models import *
from connectors.connector_funf import auth

def getAuthorization(user, scope, application):
	authorizations = Authorization.objects.filter(active=True, user=user, scope=scope, application=application)
	return authorizations


def buildUri(connector, application):
	if connector.name == 'connector_funf':
		return auth.buildUri(connector, application)
