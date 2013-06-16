import authorization_manager
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from application_manager.models import Application, GcmRegistration
from oauth2app.models import Client
from django.shortcuts import redirect
import uuid

@login_required
def grant(request):

        user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
	except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))
        client_id = request.REQUEST.get('client_id', '')
        device_id = request.REQUEST.get('device_id', '')
        gcm_id = request.REQUEST.get('gcm_id', '')

	try:
		gcm_registration = GcmRegistration.objects.get(user=user, device_id=device_id, application=Application.objects.get(client=Client.objects.get(key=client_id)))
	except: gcm_registration = None

	if gcm_id == '' and gcm_registration == None:
		#we cannot start authorization, we don\t know the gcm id
		return HttpResponse(json.dumps({'error':'please start registration from your phone'}))

	if gcm_id != '' and gcm_registration != None:
		#we should update gcm_id
		gcm_registration.gcm_id = gcm_id
		gcm_registration.save()

	#TODO: veriy params
	#TODO: check scopes that are allowed for this app

	redirect_uri = '/authorization_manager/oauth2/authorize/?'
	redirect_uri += 'client_id='+client_id
	redirect_uri += '&response_type=token'
	redirect_uri += '&scope='+','.join(scope)
	redirect_uri += '&redirect_uri='+Client.objects.get(key=client_id).redirect_uri

	return redirect(redirect_uri)

@login_required
def granted(request):
        #TODO: wrap token in authorization
        #push the token to the phone over GCM
        #get confirmation
        #redirect user back to platform

	server_nonce = str(uuid.uuid4())

        return HttpResponse('authorization granted '+server_nonce)

@login_required
def revoke(request):

        #TODO: remove scopes from the authorization

        return HttpResponse(request.user)

@login_required
def sync(request):

        #TODO: make the authorizations reflect the submit parameters

        return HttpResponse(request.user)

def confirm(request):
	return HttpResponse('confirmed')

def buildUri(connector, application):
        grant_uri = connector.grant_url+'?'
        revoke_uri = connector.revoke_url+'?'
        for param in application.params.all():
                if param.key == 'client_id':
                        grant_uri += 'client_id='+param.value+'&'
                        revoke_uri += 'client_id='+param.value+'&'
        grant_uri += 'scope=_scope_'
        revoke_uri += 'scope=_scope_'

        #TODO: add message for the empty uris, when the action needs to be initiated from somewhere else
        return {'grant_uri':grant_uri, 'revoke_uri': revoke_uri}
