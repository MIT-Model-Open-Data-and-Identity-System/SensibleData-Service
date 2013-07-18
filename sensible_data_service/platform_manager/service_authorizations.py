from django.http import HttpResponse
import json
import platform_manager
from authorization_manager import authorization_manager
from application_manager import application_manager
from collections import defaultdict


from authorization_manager import authorization_manager


def serviceAuthorizations(request):
	authentication = platform_manager.authenticate(request)
        if 'error' in authentication:
                return HttpResponse(authentication['response'])

	user = authentication['user']

	return_v = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(str))))
	applications = application_manager.getApplications()
	for application in applications:
		scopes = application_manager.getApplicationScopes(application)
		return_v[application._id]['name'] = application.name
		return_v[application._id]['owner'] = application.user.get_full_name()
		return_v[application._id]['description'] = application.description
		connectors = set()		

		for scope in scopes:
			return_v[application._id]['scopes'][scope.scope]['description'] = scope.description
			connector = scope.connector
			connectors.add(connector)
			return_v[application._id]['scopes'][scope.scope]['status'] = getAuthorizationStatus(user, application, scope)
			return_v[application._id]['scopes'][scope.scope]['connector'] = connector.name
		for connector in connectors:
			uri = createUri(user, application, connector)
			return_v[application._id]['connectors'][connector.name]['grant_uri'] = uri['grant_uri']
			return_v[application._id]['connectors'][connector.name]['revoke_uri'] = uri['revoke_uri']
			


	return HttpResponse(json.dumps({'service': dict(return_v)}))

def getAuthorizationStatus(user, application, scope):
	authorizations = authorization_manager.getAuthorization(user, application, scope)
	if len(authorizations) == 0: return 0
	return 1

def createUri(user, application, connector):
	#authorizations = authorization_manager.getAuthorization(user, application, scope)
	uri = {}
	uri = authorization_manager.buildUri(connector, application)
	return uri
