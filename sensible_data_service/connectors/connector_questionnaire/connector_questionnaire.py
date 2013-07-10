from django.http import HttpResponse
from authorization_manager import authorization_manager
import json

def upload(request):

	auth = authorization_manager.authenticate_token(request)
	if 'error' in auth:
		return HttpResponse(json.dumps(auth))
	

	#TODO process data

	return HttpResponse(auth['user'].username)
