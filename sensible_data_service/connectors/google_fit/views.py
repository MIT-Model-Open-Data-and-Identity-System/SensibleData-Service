from datetime import datetime, timedelta
from django.conf import settings
from django.template import RequestContext
import os
import logging
import httplib2

from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
from connectors.google_fit.models import CredentialsModel
from utils import SECURE_settings

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

FLOW = flow_from_clientsecrets(
	CLIENT_SECRETS,
	scope=" ".join([
		'email',
		'profile',
		'https://www.googleapis.com/auth/fitness.activity.read',
		'https://www.googleapis.com/auth/fitness.location.read',
		'https://www.googleapis.com/auth/fitness.body.read']),
	redirect_uri='http://localhost:8081/sensible-dtu/connectors/google_fit/oauth2callback')



def index(request):
	# We cannot do user auth in go_actiwe, so we use a random user
	FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, SECURE_settings.GOOGLE_FIT_USER)
	authorize_url = FLOW.step1_get_authorize_url()
	return HttpResponseRedirect(authorize_url)


def get_user_email(service):
	user_info = service.people().get(userId='me').execute()
	user_emails = user_info.get('emails')
	user_email = None
	for email in user_emails:
		if email['type'] == 'account':
			user_email = email['value']
	return user_email


def auth_return(request):

	validation = xsrfutil.validate_token(settings.SECRET_KEY, str(request.REQUEST['state']), SECURE_settings.GOOGLE_FIT_USER)
	if not validation:
		return HttpResponseBadRequest()
	credential = FLOW.step2_exchange(request.REQUEST)

	http = credential.authorize(httplib2.Http())
	service = build("plus", "v1", http=http)

	user_email = get_user_email(service)

	storage = Storage(CredentialsModel, 'google_id', user_email, 'credential')
	storage.put(credential)

	return render_to_response('google_fit/welcome.html', {'email': user_email,}, context_instance=RequestContext(request))