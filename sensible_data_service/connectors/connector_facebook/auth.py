from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import redirect
from application_manager.models import Application
import json
from .models import ConnectorFacebook

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
	url += '&scope=%s'%(','.join(['email', 'read_stream']))
	#scopes
	#return redirect
	return HttpResponse(url)


@login_required
def grantedInbound(request):
	#redirect from facebook, we get code
	#exchange code for token
	#save token as authorization with scopes
	#now we should use the token to grab data -> cron or cellery
	code = request.GET.get('code', '')
	return HttpResponse(code)

def buildInboundAuthUrl():
	grant_url = ''
	try: grant_url = Application.objects.get(connector_type='facebook_in').grant_url 
	except Application.DoesNotExist: pass
	return {'url': grant_url, 'message':'Authorized url'}


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