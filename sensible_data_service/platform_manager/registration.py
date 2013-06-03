from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
import time
import urllib2
import urllib
import json
from utils import service_config, SECURE_service_config
from django.shortcuts import redirect

def saveCode(code, user, scope):
	c = Code.objects.create(code=code, user=user, time_generated=int(time.time()))
	for s in scope:
		c.scope.add(Scope.objects.get(key=s))
	c.save()
	return True

def exchangeCodeForToken(code):
	values = {}
	values['code'] = code
	values['grant_type'] = 'authorization_code'
	values['client_id'] = SECURE_service_config.PLATFORM['client_id']
	values['client_secret'] = SECURE_service_config.PLATFORM['client_secret']
	values['redirect_uri'] = service_config.PLATFORM['redirect_uri']
	data = urllib.urlencode(values)
	req = urllib2.Request(service_config.PLATFORM['platform_uri_token'], data)
	try:
		response = urllib2.urlopen(req).read()
	except urllib2.HTTPError as e: 
		response = e.read()
		return response


	

	return json.loads(response)
	
def saveToken(user, token, code):
	c = Code.objects.get(code=code)
	t = AccessToken.objects.create(user = user, token = token['access_token'], token_type = token['token_type'], refresh_token = token['refresh_token'], expire = int(int(time.time()) + int(token['expires_in'])), code = c)
	for s in token['scope'].split(','):
		t.scope.add(Scope.objects.get(key=s))
	t.save()

	c.exchanged = True
	c.time_exchanged = int(time.time())
	c.save()

	return True

def updateUserStatus(user):
	try:
		participant = Participant.objects.get(user=user)
		participant.status = 'initiated'
		participant.save()
	except Participant.DoesNotExist:
		participant = Participant.objects.create(user=user, status='initiated')

	return True
	

@login_required
def callback(request):
	code = request.REQUEST.get('code')
	scope = request.REQUEST.get('scope').split(',')
	user = request.user

	saveCode(code, user, scope)
	token = exchangeCodeForToken(code)
	if 'error' in token:
		return redirect(service_config.PLATFORM['platform_uri_dashboard']+'?status=token_error')
	if not saveToken(user, token, code):
		return redirect(service_config.PLATFORM['platform_uri_dashboard']+'?status=save_token_error')
	
	updateUserStatus(user)
	
	return redirect(service_config.PLATFORM['platform_uri_dashboard']+'?status=success')
