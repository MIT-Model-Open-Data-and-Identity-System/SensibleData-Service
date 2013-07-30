from django.http import HttpResponse
import json
from .models import *
import platform_manager
from application_manager import application_manager
from authorization_manager import authorization_manager
from documents.models import TosAcceptance

def userStatus(request):
	authentication = platform_manager.authenticate(request)
	if 'error' in authentication:
		return HttpResponse(authentication['response'])



	user = authentication['user']
	response = {}
	response['applications'] = {}
	applications = application_manager.getApplications()
	if len(TosAcceptance.objects.filter(user=user).all()) == 0:
		return HttpResponse(json.dumps({'error':'not enrolled'}))
	
	for application in applications:
		response['applications'][application.name] = {}
		response['applications'][application.name]['description'] = application.description
		response['applications'][application.name]['uri'] = application.url
		application_scopes = application_manager.getApplicationScopes(application)
		response['applications'][application.name]['scopes'] = {}
		for scope in application_scopes:
			auth = authorization_manager.getAuthorization(user, scope, application)
			response['applications'][application.name]['scopes'][scope.scope] = {}
			response['applications'][application.name]['scopes'][scope.scope]['authorized'] = 1 if len(auth)>0 else 0 
			response['applications'][application.name]['scopes'][scope.scope]['description'] = scope.description
			response['applications'][application.name]['scopes'][scope.scope]['description_extra'] = scope.description_extra
			response['applications'][application.name]['scopes'][scope.scope]['auth_url'] = authorization_manager.buildAuthUrl(scope.connector)
		

	return HttpResponse(json.dumps(response))
