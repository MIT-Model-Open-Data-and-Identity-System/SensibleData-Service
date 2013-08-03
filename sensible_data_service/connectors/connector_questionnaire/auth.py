import authorization_manager.authorization_manager
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import redirect
from oauth2app.models import Client, AccessToken, Code
import urllib, urllib2
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import transaction
from .models import ConnectorQuestionnaire

@login_required
def grant(request):
	user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
        except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))	
	client_id = request.REQUEST.get('client_id', '')
	state = request.REQUEST.get('state', '')
	response_type = request.REQUEST.get('response_type', '')

	#TODO: fix this to dynamic reverse
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

def buildAuthUrl():
	return {'url': ConnectorQuestionnaire.objects.filter(connector_type='connector_questionnaire').all()[0].grant_url, 'message':'Authorized url'}
