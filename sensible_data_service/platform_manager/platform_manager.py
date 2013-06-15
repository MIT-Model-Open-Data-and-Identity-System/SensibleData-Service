from utils import service_config
from utils import SECURE_service_config
from .models import *
import json

def authenticate(request):
	token = request.REQUEST.get('access_token')
        host = request.META['REMOTE_ADDR']
	if not host in service_config.PLATFORM['ip_addr']: return {'error': 'ip address not authorized', 'response': json.dumps({'error': 'ip address not authorized'})}

	try: user = PlatformAccessToken.objects.get(token=token).user
        except PlatformAccessToken.DoesNotExist: return {'error': 'no user found', 'response': json.dumps({'error': 'no user found'})}

	return {'ok':'authenticated', 'user': user}
