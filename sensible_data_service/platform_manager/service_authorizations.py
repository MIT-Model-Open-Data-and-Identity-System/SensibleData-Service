from django.http import HttpResponse
import json
import platform_manager
from authorization_manager import authorization_manager
from utils import service_config

def serviceAuthorizations(request):
	authentication = platform_manager.authenticate(request)
        if 'error' in authentication:
                return HttpResponse(json.dumps(authentication))

	user = authentication['user']

	authorizationManager = authorization_manager.AuthorizationManager()
	

	#connectors = 
	#for connector in service_config.CONNECTORS:
		
	

	return HttpResponse(json.dumps({'user': str(user)}))
