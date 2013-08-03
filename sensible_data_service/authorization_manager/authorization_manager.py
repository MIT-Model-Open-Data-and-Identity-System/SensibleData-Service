from .models import *
from application_manager.models import Application
import hashlib
import uuid
import time
import urllib, urllib2
import json
from oauth2app.authenticate import Authenticator, AuthenticationException
from django.conf import settings
from documents.models import TosAcceptance
from django.db import transaction

from connectors import connector_funf
from connectors import connector_questionnaire

def buildAuthUrl(connector):
	if connector.connector_type == 'connector_funf':
		return connector_funf.auth.buildAuthUrl()
	return {'error':'no valid connector provided'}

def getAuthorization(user, scope, application):
	authorizations = Authorization.objects.filter(active=True, user=user, scope=scope, application=application)
	return authorizations
	
def getAuthorizationForToken(scope, token):
	auth = Authorization.objects.filter(scope=Scope.objects.get(scope = scope),\
		access_token=AccessToken.objects.get(access_token=token),\
		active = True)
	if len(auth) > 0:
		return auth[0]
	else:
		return None

def createAuthorization(response):
	access_token_to_query = response['access_token']
	access_token = AccessToken.objects.get(token=str(access_token_to_query))
	
	if len(TosAcceptance.objects.filter(user=access_token.user).all()) == 0:        
		return {'error':'user is not enrolled in the study'}

	server_nonce = hashlib.sha256(str(uuid.uuid4())).hexdigest()
	for scope in access_token.scope.all():
		authorization = Authorization.objects.create(user=access_token.user, scope=scope, application=Application.objects.get(client=access_token.client), access_token=access_token, nonce=server_nonce, active=True, activated_at=time.time())



def token(code, client_id, client_secret, redirect_uri):
	values = {}
	values['code'] = code
	values['grant_type'] = 'authorization_code'
	values['client_id'] = client_id
	values['client_secret'] = client_secret
	values['redirect_uri'] = redirect_uri
	data = urllib.urlencode(values)

	request_uri = settings.BASE_URL+'authorization_manager/oauth2/token'

	req = urllib2.Request(request_uri, data)
	try: response = urllib2.urlopen(req).read()
	except urllib2.HTTPError as e:
		response = e.read()
		return response

	transaction.commit()
	createAuthorization(json.loads(response))
	return response

def refresh_token(refresh_token, client_id, client_secret, redirect_uri, scope):
	values = {}
	values['refresh_token'] = refresh_token
	values['grant_type'] = 'refresh_token'
	values['client_id'] = client_id
	values['client_secret'] = client_secret
	values['redirect_uri'] = redirect_uri
	values['scope'] = scope
	data = urllib.urlencode(values)
	request_uri = settings.BASE_URL+'authorization_manager/oauth2/token'

	req = urllib2.Request(request_uri, data)
	try: response = urllib2.urlopen(req).read()
	except urllib2.HTTPError as e:
		response = e.read()
		return response

	transaction.commit()
	createAuthorization(json.loads(response))
	return response

def authenticate_token(request, scope=None, client_id=None):
	authenticator = Authenticator()
	try: authenticator.validate(request)
   	except AuthenticationException: return {'error': authenticator.error.message}
	auth_client_id = AccessToken.objects.get(token=request.REQUEST.get('bearer_token')).client.key
	auth_scope = [x.scope for x in authenticator.scope]
	if type(scope) == str: scope = [scope]
	if not scope == None:
		if not set(scope).issubset(set(auth_scope)):
			return {'error':'token not authorized for this scope'}

	if not client_id == None:
		if not client_id == auth_client_id:
			return {'error':'token not authorized for this client_id'}

	return {'ok': 'success', 'user': authenticator.user, 'scope': auth_scope, 'client_id': auth_client_id}


def registerGcm(request, scope):
	device_id = request.REQUEST.get('device_id', '')
	gcm_id = request.REQUEST.get('gcm_id', '')
	access_token = request.REQUEST.get('access_token', '')
	auth = authenticate_token(request, scope)
	if 'error' in auth: return auth
	user = auth['user']
	client_id = auth['client_id']
	if gcm_id == '': return {'error':'no gcm_id provided'}
	if device_id == '': return {'error':'no device_id provided'}

	try:
		device = Device.objects.get(user=user, device_id=device_id)
	except Device.DoesNotExist:
		device = Device.objects.create(user=user, device_id=device_id)

	try:
		gcm_registration = GcmRegistration.objects.get(user=user, device=device, application=Application.objects.get(client=Client.objects.get(key=client_id)))
		gcm_registration.gcm_id = gcm_id
		gcm_registration.save()

	except GcmRegistration.DoesNotExist:
		gcm_registration = GcmRegistration.objects.create(user=user, device=device, application=Application.objects.get(client=Client.objects.get(key=client_id)), gcm_id=gcm_id)
		gcm_registration.save()
	except Application.DoesNotExist:
		return {'error':'application does not exist'}
	except Client.DoesNotExist:
		return {'error':'client does not exist'}

	return {'ok':'gcm registration complete'}
