from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect
from application_manager.models import Application
import json
from .models import ConnectorFacebook
from connectors.models import Scope, Connector
import urllib2
import time
from documents.models import InformedConsent
from authorization_manager.models import Authorization
from django.conf import settings

def decodeParams(s):
	s = s.strip()
	s = s.replace('\r','')
	s = s.replace('\n','')
	return json.loads(s)

@login_required
def grantInbound(request):
	url = 'https://www.facebook.com/dialog/oauth?'
	params = decodeParams(Application.objects.get(connector_type='facebook_in').extra_params)
	url += 'client_id=%s'%params['client_id']
	url += '&redirect_uri=%s'%ConnectorFacebook.objects.get(connector_type='connector_facebook_in').grant_url
	url += '&response_type=code'
	scopes_checked = set()
	for x in request.GET.items():
		try: 
			if x[1] == 'checked': scopes_checked.add(x[0])
		except: continue

	scopes = set()
	for scope in scopes_checked:
		try:
			scopes.add(Scope.objects.get(scope=scope.split('scope_')[1]).description_extra)
		except: continue

	scopes_str = set()
	for scope in scopes:
		for s in scope.split('facebook:')[1].split(','):
			scopes_str.add(s.strip())


	url += '&scope=%s'%','.join(scopes_str)
	return redirect(url)


@login_required
def grantedInbound(request):
	error = request.GET.get('error', '')
	if not error == '':
		error_description = request.GET.get('error', '')
		r = redirect(settings.PLATFORM['platform_uri'])
		r['Location'] += '?status=auth_error&message='+error_description
		return r


	code = request.GET.get('code', '')
	url = 'https://graph.facebook.com/oauth/access_token?'
	params = decodeParams(Application.objects.get(connector_type='facebook_in').extra_params)
	url += 'client_id=%s'%params['client_id']
	url += '&redirect_uri=%s'%ConnectorFacebook.objects.get(connector_type='connector_facebook_in').grant_url
	url += '&client_secret=%s'%params['client_secret']
	url += '&code=%s'%code
	
	try:
		response = urllib2.urlopen(url).read()
		access_token = response.split('&')[0].split('access_token=')[1]
	except: return HttpResponse(json.dumps({'error':'could not get access token (code 4718)'}))

	url = 'https://graph.facebook.com/oauth/access_token?'
	url += 'grant_type=fb_exchange_token&'
	url += 'client_id=%s&'%params['client_id']
	url += 'client_secret=%s&'%params['client_secret']
	url += 'fb_exchange_token=%s'%access_token
	
	try:
		response = urllib2.urlopen(url).read()
		access_token = response.split('&')[0].split('access_token=')[1]
	except: return HttpResponse(json.dumps({'error':'could not exchange access token (code 0001)'}))



	url = 'https://graph.facebook.com/debug_token?'
	url += 'input_token=%s&'%access_token
	url += 'access_token=%s'%params['client_access_token']

	try:
		response = json.loads(urllib2.urlopen(url).read())
	except: return HttpResponse(json.dumps({'error':'could not introspect token (code 0002)'}))

	granted_scopes = response['data']['scopes']
	user_id = response['data']['user_id']
	expires_at = int(response['data']['expires_at'])

	authorizations_granted = set()
	for scope in granted_scopes:
		for our_scope in Scope.objects.filter(connector=Connector.objects.get(connector_type='connector_facebook_in')).all():
			if scope in our_scope.description_extra: authorizations_granted.add(our_scope)
	
	user = request.user
	if len(InformedConsent.objects.filter(user=user).all()) == 0:
		        return HttpResponse(json.dumps({'error':'user is not enrolled in the study (code 0003)'}))

	for scope in authorizations_granted:
		Authorization.objects.create(user=user, scope=scope, application=Application.objects.get(connector_type='facebook_in'), active=True, activated_at = int(time.time()), payload = json.dumps({'expires_at': expires_at, 'access_token': access_token, 'user_id': user_id}))

	return redirect(settings.PLATFORM['platform_uri'])

def buildInboundAuthUrl():
	grant_url = ''
	try: grant_url = Application.objects.get(connector_type='facebook_in').grant_url 
	except Application.DoesNotExist: pass
	return {'url': grant_url, 'message':'Authorized url'}

def getAllInboundAuth():
	return Authorization.objects.filter(active=True, application=Application.objects.get(connector_type='facebook_in')).all()

def getResourceMappings():
	return json.loads(Application.objects.get(connector_type='facebook_in').extra_params)['scope_resource_mapping']


@login_required
def grant(request):
	user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
	except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))
	client_id = request.REQUEST.get('client_id', '')
	state = request.REQUEST.get('state', '')
	response_type = request.REQUEST.get('response_type', '')

	redirect_uri = settings.BASE_URL + 'authorization_manager/oauth2/authorize/?'
	redirect_uri += '&client_id='+client_id
	redirect_uri += '&response_type='+response_type
	redirect_uri += '&scope='+','.join(scope)
	redirect_uri += '&redirect_uri='+Client.objects.get(key=client_id).redirect_uri+'&state='+state

	return redirect(redirect_uri)


@csrf_exempt
@transaction.commit_manually
def token(request):
	code = request.POST.get('code')
	client_id = request.POST.get('client_id')
	client_secret = request.POST.get('client_secret')
	redirect_uri = request.POST.get('redirect_uri')

	response = authorization_manager.authorization_manager.token(code, client_id, client_secret, redirect_uri)
	transaction.commit()
	return HttpResponse(response)


@csrf_exempt
@transaction.commit_manually
def refresh_token(request):
	refresh_token = request.POST.get('refresh_token')
	client_id = request.POST.get('client_id')
	client_secret = request.POST.get('client_secret')
	redirect_uri = request.POST.get('redirect_uri')
	scope = request.POST.get('scope')

	response = authorization_manager.authorization_manager.refresh_token(refresh_token, client_id, client_secret, redirect_uri, scope)
	transaction.commit()
	return HttpResponse(response)

def buildAuthUrl(application=None):
	grant_url = ''
	if not application == None:
		try: grant_url = application.grant_url
		except: return {'url': grant_url, 'message': 'The application is not available at the moment'}
	return {'url': grant_url, 'message':'Authorized url'}
