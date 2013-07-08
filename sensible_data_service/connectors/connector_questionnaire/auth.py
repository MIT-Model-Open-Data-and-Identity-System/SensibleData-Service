import authorization_manager
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import redirect
from oauth2app.models import Client, AccessToken

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
	
	return redirect(redirect_uri)
