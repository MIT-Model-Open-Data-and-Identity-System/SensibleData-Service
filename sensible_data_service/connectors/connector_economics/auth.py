import authorization_manager.authorization_manager
from application_manager import gcm_server
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from application_manager.models import Application, GcmRegistration, Device
from authorization_manager.models import Authorization
from oauth2app.models import Client, AccessToken
from django.shortcuts import redirect
import uuid
import hashlib
from connectors.models import Scope
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.db import transaction

@login_required
def initiateGrant(request):
	return HttpResponse('TODO: display message about starting the process on the device')


@login_required
def grant(request):
	user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
	except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))
	client_id = request.REQUEST.get('client_id', '')
	device_id = request.REQUEST.get('device_id', '')
	gcm_id = request.REQUEST.get('gcm_id', '')

	try: Application.objects.get(client=Client.objects.get(key=client_id))
	except Application.DoesNotExist: return HttpResponse(json.dumps({'error':'client_id (Application) does not exist'}))
	except Client.DoesNotExist: return HttpResponse(json.dumps({'error':'client_id (Client) does not exist'}))

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

	# TODO: figure out why /authorize/ is not working properly (seems to be the one that should be used)
	# redirect_uri = settings.ROOT_URL+'authorization_manager/oauth2/authorize_refreshed/?'
	redirect_uri = settings.ROOT_URL+'authorization_manager/oauth2/authorize/?'
	redirect_uri += 'client_id='+client_id
	redirect_uri += '&response_type=code'
	redirect_uri += '&scope='+','.join(final_scopes)
	redirect_uri += '&redirect_uri='+Client.objects.get(key=client_id).redirect_uri
	# redirect_uri += '&state='+gcm_id

	return redirect(redirect_uri)

@login_required
def granted(request):

	code = request.REQUEST.get('code', '')
	gcm_id = request.REQUEST.get('state', '')

	# response = gcm_server.sendNotification(gcm_id, data={'title': 'Authenticated', 'timestamp': time.time(), 'body':'Successfully authenticated', 'code': code}, type='auth_code')

	return render_to_response('authorization_in_progress.html', {}, RequestContext(request))


@csrf_exempt
@transaction.commit_manually
def token(request):
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
def refresh_token(request):
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


def gcm(request):
	return HttpResponse(json.dumps(authorization_manager.authorization_manager.registerGcm(request, scope = 'connector_economics.push_notifications')))

def buildAuthUrl(application = None):
	return {'url':'', 'message':'Please start registration from your phone'}
	# grant_url = ''
	# message = 'Auhtorize url'
	# if not application == None:
	# 	try:
	# 		grant_url = application.grant_url
	# 		try:
	# 			message = json.loads(application.extra_params)['auth_message']
	# 		except: pass
	# 	except:
	# 		return {'url': grant_url, 'message': 'The application is not available at the moment'}

	# return {'url': grant_url, 'message': message}
