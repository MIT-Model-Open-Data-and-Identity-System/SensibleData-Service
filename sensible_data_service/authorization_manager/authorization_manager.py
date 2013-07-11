from .models import *
from connectors.connector_funf import auth
from application_manager.models import Application
import hashlib
import uuid
import time
import urllib, urllib2
import json
from oauth2app.authenticate import Authenticator, AuthenticationException

def getAuthorization(user, scope, application):
	authorizations = Authorization.objects.filter(active=True, user=user, scope=scope, application=application)
	return authorizations

def createAuthorization(response):
	access_token = AccessToken.objects.get(token=response['access_token'])
        server_nonce = hashlib.sha256(str(uuid.uuid4())).hexdigest()
        for scope in access_token.scope.all():
                authorization = Authorization.objects.create(user=access_token.user, scope=scope, application=Application.objects.get(client=access_token.client), access_token=access_token, nonce=server_nonce, active=True, activated_at=time.time())

def buildUri(connector, application):
	if connector.name == 'connector_funf':
		return auth.buildUri(connector, application)


def token(code, client_id, client_secret, redirect_uri):
	values = {}
        values['code'] = code
        values['grant_type'] = 'authorization_code'
        values['client_id'] = client_id
        values['client_secret'] = client_secret
        values['redirect_uri'] = redirect_uri
        data = urllib.urlencode(values)

	request_uri = 'http://166.78.249.214:8082/authorization_manager/oauth2/token'

        req = urllib2.Request(request_uri, data)
        try:
                response = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
                response = e.read()
                return response
	

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

	
	request_uri = 'http://166.78.249.214:8082/authorization_manager/oauth2/token'

        req = urllib2.Request(request_uri, data)
        try:
                response = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
                response = e.read()
                return response

	createAuthorization(json.loads(response))
        return response

def authenticate_token(request):
	authenticator = Authenticator()
	try: authenticator.validate(request)
   	except AuthenticationException: return {'error':'authentication error'}
	return {'ok':'success', 'user':authenticator.user}
