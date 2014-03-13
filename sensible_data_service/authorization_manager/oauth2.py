#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from uni_form.helpers import FormHelper, Submit, Reset
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
from oauth2app.models import *
from oauth2app.consts import CODE, TOKEN, CODE_AND_TOKEN
from .forms import AuthorizeForm
from django.core.urlresolvers import reverse
from documents.models import InformedConsent
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import json
from datetime import datetime
from django.shortcuts import redirect
from urlparse import urlparse, parse_qs
from accounts.models import UserRole

@login_required
def missing_redirect_uri(request):
    return render_to_response(
        'oauth2/missing_redirect_uri.html',
        {},
        RequestContext(request))


def authorize(request):
#	try:
#		sessions = Session.objects.filter(expire_date__gte=datetime.now())
#		for session in sessions:
#			data = session.get_decoded()
#			try: user = User.objects.filter(id=data.get('_auth_user_id', None))[0]
#			except: continue
#			if request.user == user:
#				session.delete()
#	except: pass
	return redirect(settings.ROOT_URL+'authorization_manager/oauth2/authorize_refreshed/?'+request.GET.urlencode())

@login_required
def authorize_refreshed(request):
	authorizer = Authorizer(response_type=CODE_AND_TOKEN)
	try:
		authorizer.validate(request)
	except MissingRedirectURI, e:
		return HttpResponseRedirect(settings.ROOT_URL+"authorization_manager/oauth2/missing_redirect_uri")
	except AuthorizationException, e:
		# The request is malformed or invalid. Automatically
		# redirects to the provided redirect URL.
		return authorizer.error_redirect()
	if request.method == 'GET':
        # Make sure the authorizer has validated before requesting the client
        # or access_ranges as otherwise they will be None.
		roles = []
		try: roles = [x.role for x in UserRole.objects.get(user=authorizer.user).roles.all()]
		except: pass

		if (not 'researcher' in roles) and (len(InformedConsent.objects.filter(user=authorizer.user).all()) == 0):
			return render_to_response('not_enrolled.html', {'platform_url':settings.PLATFORM['platform_uri']}, RequestContext(request))

		#TODO make this is into a policy module rather than hardcoded policy(place, user) return True/False
		if not 'researcher' in roles:
			authorizer.access_ranges = [x for x in authorizer.access_ranges if 'researcher' not in x.scope]


		template = {
				"client":authorizer.client,
				"scopes":authorizer.access_ranges}
		template["form"] = AuthorizeForm()
		helper = FormHelper()
		no_submit = Submit('connect','No', css_class='btn btn-large')
		helper.add_input(no_submit)
		yes_submit = Submit('connect', 'Yes', css_class='btn btn-large btn-success')
		helper.add_input(yes_submit)
		helper.form_action = reverse('oauth2_authorize_refreshed') + '?%s' % authorizer.query_string
		helper.form_method = 'POST'
		template["helper"] = helper
		return render_to_response(
				'oauth2/authorize.html',
				template,
				RequestContext(request))
	elif request.method == 'POST':
		#TODO here we should prevent event the access token from being created according to policy
		form = AuthorizeForm(request.POST)
		if form.is_valid():
			if request.POST.get("connect") == "Yes":
				return authorizer.grant_redirect()
			else:
				return authorizer.error_redirect()
	return HttpResponseRedirect(settings.ROOT_URL)
