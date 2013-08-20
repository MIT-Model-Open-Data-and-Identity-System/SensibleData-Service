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
from application_manager.models import Application, GcmRegistration, Device
from connectors.models import Scope
from django.shortcuts import render_to_response
from django.template import RequestContext

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


@login_required
def grant_mobile(request):
	user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
	except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))
	client_id = request.REQUEST.get('client_id', '')
	device_id = request.REQUEST.get('device_id', '')
	gcm_id = request.REQUEST.get('gcm_id', '')
	try: Application.objects.get(client=Client.objects.get(key=client_id))
	except Application.DoesNotExist: return HttpResponse(json.dumps({'error':'client_id does not exist'}))
	except Client.DoesNotExist: return HttpResponse(json.dumps({'error':'client_id does not exist'}))
	try: gcm_registration = GcmRegistration.objects.get(user=user, device=Device.objects.get(user=user, device_id=device_id), application=Application.objects.get(client=Client.objects.get(key=client_id)))
	except: gcm_registration = None
	if gcm_id == '' and gcm_registration == None:
		#we cannot start authorization, we don't know the gcm id
		#TODO nice error page
		return HttpResponse(json.dumps({'error':'please start registration from your phone'}))
	if device_id == '':
		return HttpResponse(json.dumps({'error':'please start registration from your phone'}))

	try:
		device = Device.objects.get(user=user, device_id=device_id)
	except Device.DoesNotExist:
		device = Device.objects.create(user=user, device_id=device_id)


	if not gcm_registration == None and not gcm_id == '':
		#update gcm_id
		gcm_registration.gcm_id = gcm_id
		gcm_registration.save()

	if gcm_registration == None:
		gcm_registration = GcmRegistration.objects.create(user=user, device=device, gcm_id=gcm_id, application=Application.objects.get(client=Client.objects.get(key=client_id)))
		gcm_registration.save()
	
	gcm_id = gcm_registration.gcm_id

	allowed_scopes = Application.objects.get(client=Client.objects.get(key=client_id)).scopes.all()

	final_scopes = []

	for s in scope:
		try: ss = Scope.objects.get(scope=s)
		except Scope.DoesNotExist: continue
		if ss in allowed_scopes: final_scopes.append(ss.scope)

	if len(final_scopes) == 0:
		return HttpResponse(json.dumps({'error':'no valid scope provided'}))


	redirect_uri = settings.ROOT_URL+'authorization_manager/oauth2/authorize/?'
	redirect_uri += 'client_id='+client_id
	redirect_uri += '&response_type=code'
	redirect_uri += '&scope='+','.join(final_scopes)
	redirect_uri += '&redirect_uri='+Client.objects.get(key=client_id).redirect_uri
	redirect_uri += '&state='+gcm_id

	return redirect(redirect_uri)

@login_required
def granted_mobile(request):
	error = request.REQUEST.get('error', '')
	code = request.REQUEST.get('code', '')
	#gcm_id = request.REQUEST.get('state', '')
	gcm_id = 'XXX'

	return render_to_response('authorization_in_progress.html', {}, RequestContext(request))


@csrf_exempt
@transaction.commit_manually
def token_mobile(request):
	code = request.POST.get('code')
	client_id = request.POST.get('client_id')
	client_secret = request.POST.get('client_secret')
	device_id = request.POST.get('device_id')
	redirect_uri = Client.objects.get(key=client_id).redirect_uri #get causes transaction!

	response = authorization_manager.authorization_manager.token(code, client_id, client_secret, redirect_uri, device_id=device_id)
	if not 'error' in response:
		token = AccessToken.objects.get(token = json.loads(response)['access_token'])
		#we generate long-lived (10 years) tokens, still supporting endpoint for refresh that should be performed every N days
		#those are not strictly OAuth2 tokens in this context, they are not used in the connection but as authorization code...
		token.expire += 10*365*24*60*60
		token.save()

	transaction.commit()
	return HttpResponse(response)
	transaction.rollback()

@csrf_exempt
@transaction.commit_manually
def refresh_token_mobile(request):
	refresh_token = request.POST.get('refresh_token')
	client_id = request.POST.get('client_id')
	client_secret = request.POST.get('client_secret')
	device_id = request.POST.get('device_id')

	redirect_uri = Client.objects.get(key=client_id).redirect_uri

	scope = ','.join([x.scope for x in AccessToken.objects.get(refresh_token=refresh_token).scope.all()])


	response = authorization_manager.authorization_manager.refresh_token(refresh_token, client_id, client_secret, redirect_uri, scope, device_id=device_id)
	transaction.commit()
	if not 'error' in response:
		token = AccessToken.objects.get(token = json.loads(response)['access_token'])
		#we generate long-lived (10 years) tokens, still supporting endpoint for refresh that should be performed every N days
		#those are not strictly OAuth2 tokens in this context, they are not used in the connection but as authorization code...
		token.expire += 10*365*24*60*60
		token.save()

	transaction.commit()
	return HttpResponse(response)
	transaction.rollback()


def gcm(request):
	    return HttpResponse(json.dumps(authorization_manager.authorization_manager.registerGcm(request, scope = 'connector_raw.location')))

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
	message = 'Auhtorize url'
	if not application == None:
		try: 
			grant_url = application.grant_url
			try:
				message = json.loads(application.extra_params)['auth_message']
			except: pass
		except: 
			return {'url': grant_url, 'message': 'The application is not available at the moment'}

	return {'url': grant_url, 'message': message}
