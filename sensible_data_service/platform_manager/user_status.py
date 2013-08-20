from django.http import HttpResponse
import json
from .models import *
import platform_manager
from application_manager import application_manager
import authorization_manager.authorization_manager
from documents.models import InformedConsent

def userStatus(request):
	authentication = platform_manager.authenticate(request)
	if 'error' in authentication:
		return HttpResponse(authentication['response'])



	user = authentication['user']
	response = {}
	response['applications'] = {}
	applications = application_manager.getApplications()
	if len(InformedConsent.objects.filter(user=user).all()) == 0:
		return HttpResponse(json.dumps({'error':'not enrolled'}))
	
	for application in applications:
		response['applications'][application.name] = {}
		response['applications'][application.name]['description'] = application.description
		response['applications'][application.name]['uri'] = application.url
		application_scopes = application_manager.getApplicationScopes(application)
		response['applications'][application.name]['scopes'] = {}
		for scope in application_scopes:
			if 'researcher' in scope.scope: continue
			auth = authorization_manager.authorization_manager.getAuthorization(user, scope, application)
			response['applications'][application.name]['scopes'][scope.scope] = {}
			response['applications'][application.name]['scopes'][scope.scope]['authorized'] = 1 if len(auth)>0 else 0 
			response['applications'][application.name]['scopes'][scope.scope]['description'] = scope.description
			response['applications'][application.name]['scopes'][scope.scope]['description_extra'] = scope.description_extra
			response['applications'][application.name]['scopes'][scope.scope]['auth_url'] = authorization_manager.authorization_manager.buildAuthUrl(scope.connector, application)
		

	return HttpResponse(json.dumps(response))
