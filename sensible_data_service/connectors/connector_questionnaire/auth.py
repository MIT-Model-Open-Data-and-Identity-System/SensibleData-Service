import authorization_manager
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import redirect
from oauth2app.models import Client, AccessToken, Code
import urllib, urllib2
from django.views.decorators.csrf import csrf_exempt
from authorization_manager import authorization_manager
import json

@login_required
def grant(request):
	user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
        except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))	
	client_id = request.REQUEST.get('client_id', '')
	state = request.REQUEST.get('state', '')
	response_type = request.REQUEST.get('response_type', '')

	redirect_uri = '/authorization_manager/oauth2/authorize/?'
        redirect_uri += 'client_id='+client_id
        redirect_uri += '&response_type='+response_type
        redirect_uri += '&scope='+','.join(scope)
        redirect_uri += '&redirect_uri='+Client.objects.get(key=client_id).redirect_uri+'&state='+state
        #redirect_uri += '&redirect_uri='+'/authorization_manager/connector_questionnaire/auth/granted/'+'&state='+state
	
	return redirect(redirect_uri)


@csrf_exempt
def token(request):
	code = request.POST.get('code')
	client_id = request.POST.get('client_id')
	client_secret = request.POST.get('client_secret')
	redirect_uri = request.POST.get('redirect_uri')

	response = authorization_manager.token(code, client_id, client_secret, redirect_uri)
        return HttpResponse(response)

@csrf_exempt
def refresh_token(request):
	refresh_token = request.POST.get('refresh_token')
	client_id = request.POST.get('client_id')
	client_secret = request.POST.get('client_secret')
	redirect_uri = request.POST.get('redirect_uri')
	scope = request.POST.get('scope')
	
	response = authorization_manager.refresh_token(refresh_token, client_id, client_secret, redirect_uri, scope)
        return HttpResponse(response)
