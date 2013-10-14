from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from accounts.models import UserRole
from application_manager import application_manager
import authorization_manager.authorization_manager
import time
from sensible_data_service import settings as service_settings

@login_required
def researcher(request):
	roles = []
	try: roles = [x.role for x in UserRole.objects.get(user=request.user).roles.all()]
	except: pass

	values = {}
	applications = application_manager.getApplications()
	for application in applications:
		if not application.connector_type == 'data_viewer': continue
		values[application.name] = {}
		values[application.name]['uri'] = application.url
		values[application.name]['description'] = application.description
		application_scopes = application_manager.getApplicationScopes(application)
		values[application.name]['scopes'] = {}
		for scope in application_scopes:
			if not 'researcher' in scope.scope: continue
			auth = authorization_manager.authorization_manager.getAuthorization(request.user, scope, application)
			auth = [x for x in auth if x.access_token.expire > time.time()]

			values[application.name]['scopes'][scope.scope] = {}
			values[application.name]['scopes'][scope.scope]['authorized'] = 1 if len(auth)>0 else 0
			values[application.name]['scopes'][scope.scope]['authorization'] = auth
			values[application.name]['scopes'][scope.scope]['description'] = scope.description
			values[application.name]['scopes'][scope.scope]['description_extra'] = scope.description_extra
			values[application.name]['scopes'][scope.scope]['auth_url'] = authorization_manager.authorization_manager.buildAuthUrl(scope.connector, application)



	if not 'researcher' in roles:
		return render_to_response('researcher.html', {'authorized': False}, context_instance=RequestContext(request))
	return render_to_response('researcher.html', {'authorized': True, 'application_values': values}, context_instance=RequestContext(request))

