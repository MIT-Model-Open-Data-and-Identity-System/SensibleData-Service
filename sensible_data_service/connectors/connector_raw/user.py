from django.http import HttpResponse
import bson.json_util as json
from authorization_manager import authorization_manager
from utils import database
from django.shortcuts import render_to_response
from accounts.models import UserRole
from django.contrib.auth.models import User
import re
import urllib
import time
from connector_utils import *
from sensible_audit import audit

log = audit.getLogger(__name__)

def user(request):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))
	accepted_scopes = set(['connector_raw.all_data', 'connector_raw.all_data_researcher'])
	auth = authorization_manager.authenticate_token(request)

	if 'error' in auth:
		log.error(audit.message(request, auth))
		return HttpResponse(json.dumps(auth), status=401)
	
	auth_scopes = set([x for x in auth['scope']])
	if len(accepted_scopes & auth_scopes) == 0:
		log.error(audit.message(request, {'error':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}))
		return HttpResponse(json.dumps({'error':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}), status=401)

	is_researcher = False
	for s in auth_scopes:
		if s == 'connector_raw.all_data_researcher': is_researcher = True

	users_to_return = buildUsersToReturn(auth['user'], request, is_researcher = is_researcher)
	roles = []
	try: roles = [x.role for x in UserRole.objects.get(user=auth['user']).roles.all()]
	except: pass

	own_data = False
	if len(users_to_return) == 1 and users_to_return[0] == auth['user'].username: own_data = True
	
	return userBuild(request, users_to_return, decrypted = decrypted, own_data = own_data, roles = roles)

def buildUsersToReturn(auth_user, request, is_researcher = False):
	users_to_return = []
	if not is_researcher:
		users_to_return.append(auth_user.username)
		return users_to_return

	if is_researcher:
		requested_users = [user for user in request.REQUEST.get('users','').split(',') if len(user) > 0]
		if len(requested_users) > 0:
			users_to_return = requested_users
		else: users_to_return.append('all')
	return users_to_return


def userBuild(request, users_to_return, decrypted = False, own_data = False, roles = []):
	
	_start_time = time.time()

	pretty = booleanize(request.REQUEST.get('pretty', False))
	response = {}
	response['meta'] = {}

	db = database.Database()

	collection= 'device_inventory'

	response['results'] = [x for x in db.getDocuments(query={}, collection=collection).distinct('user') if x in users_to_return or 'all' in users_to_return]

	response['meta']['execution_time_seconds'] = time.time()-_start_time
	response['meta']['status'] = {'status':'OK','code':200, 'desc':''}
	


	if decrypted:
		pass

	if pretty:
		log.info(audit.message(request, response['meta']))
		return render_to_response('pretty_json.html', {'response': json.dumps(response, indent=2)})
	else:
		log.info(audit.message(request, response['meta']))
		return HttpResponse(json.dumps(response), content_type="application/json", status=response['meta']['status']['code'])
	return HttpResponse('hello decrypted')
