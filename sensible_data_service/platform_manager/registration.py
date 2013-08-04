from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
import time
import urllib2
import urllib
import json
from utils import SECURE_settings
from django.shortcuts import redirect
from django.conf import settings
from documents import create_document
from django.contrib.sessions.models import Session

def saveCode(code, user, scope):
	c = PlatformCode.objects.create(code=code, user=user, time_generated=int(time.time()))
	for s in scope:
		c.scope.add(PlatformScope.objects.get(key=s))
	c.save()
	return True

def exchangeCodeForToken(code):
	values = {}
	values['code'] = code
	values['grant_type'] = 'authorization_code'
	values['client_id'] = SECURE_settings.PLATFORM['client_id']
	values['client_secret'] = SECURE_settings.PLATFORM['client_secret']
	values['redirect_uri'] = settings.PLATFORM['redirect_uri']
	data = urllib.urlencode(values)
	req = urllib2.Request(settings.PLATFORM['platform_uri_token'], data)
	try:
		response = urllib2.urlopen(req).read()
	except urllib2.HTTPError as e: 
		response = e.read()
		return response

	return json.loads(response)
	
def saveToken(user, token, code):
	c = PlatformCode.objects.get(code=code)
	t = PlatformAccessToken.objects.create(user = user, token = token['access_token'], token_type = token['token_type'], refresh_token = token['refresh_token'], expire = int(int(time.time()) + int(token['expires_in'])), code = c)
	for s in token['scope'].split(','):
		t.scope.add(PlatformScope.objects.get(key=s))
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
def authorize(request):
	Session.objects.all().delete()
	url = settings.PLATFORM['platform_uri']+'oauth2/oauth2/authorize/'
	url += '?redirect_uri='+settings.PLATFORM['redirect_uri']
	url += '&scope='+'enroll'
	url += '&client_id='+SECURE_settings.PLATFORM['client_id']
	url += '&response_type='+'code'
	#return HttpResponse(url)
	return redirect(url)

@login_required
def callback(request):
	error = request.REQUEST.get('error', '')
	if not error == '':
		return redirect(settings.PLATFORM['platform_uri']+'?status=auth_error')

	code = request.REQUEST.get('code')
	scope = request.REQUEST.get('scope').split(',')
	user = request.user

	saveCode(code, user, scope)
	token = exchangeCodeForToken(code)
	if 'error' in token:
		return redirect(settings.PLATFORM['platform_uri']+'?status=token_error')
	if not saveToken(user, token, code):
		return redirect(settings.PLATFORM['platform_uri']+'?status=save_token_error')
	
	if 'enroll' in scope:
		create_document.createInformedConsent(user, 'da')
	
	#return HttpResponse(json.dumps(scope))
	return redirect(settings.PLATFORM['platform_uri']+'?status=success&message=You are now enrolled!')
