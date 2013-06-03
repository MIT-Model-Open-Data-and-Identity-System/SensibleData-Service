from django.http import HttpResponse
from utils import service_config
import json
from .models import *
import platform_manager

def userStatus(request):
	authentication = platform_manager.authenticate(request)
	if 'error' in authentication:
		return HttpResponse(json.dumps(authentication))


	user = authentication['user']
	response = {'user_status':'unknown'}
	
	try: response['user_status'] = user.participant.status
	except Participant.DoesNotExist: return HttpResponse(json.dumps(response))

	return HttpResponse(json.dumps(response))
