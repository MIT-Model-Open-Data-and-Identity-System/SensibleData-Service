import time
import datetime
from django.contrib.auth.models import User

from django.http import HttpResponse
import bson.json_util as json
from django.shortcuts import render_to_response

from authorization_manager import authorization_manager
from connectors.connector_raw.raw_data import array_to_csv
from db_access.named_queries.named_queries import NAMED_QUERIES
from user_metadata import metadata
from user_metadata.models import StaticMetadata

from utils import db_wrapper
from accounts.models import UserRole
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
	
	return user_metadata(request, users_to_return, decrypted = decrypted, own_data = own_data, roles = roles)

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


def user_metadata(request, users_to_return, decrypted = False, own_data = False, roles = []):

	_start_time = time.time()

	pretty = booleanize(request.REQUEST.get('pretty', False))
	csv = booleanize(request.REQUEST.get('csv', False))

	response = {}
	response['meta'] = {}

	timestamp = request.REQUEST.get("timestamp", datetime.datetime.now())
	metadata_attributes = request.REQUEST.get("attributes")
	metadata_attributes = [] if not metadata_attributes else metadata_attributes.split(",")

	if 'all' in users_to_return:
		users = User.objects.all()
		users_to_return = [user.username for user in users if not hasattr(user, "userrole")]
	users_with_metadata = metadata.get_metadata_for_users(users_to_return, timestamp, metadata_attributes=metadata_attributes)

	users_without_metadata = set(users_to_return) - set(users_with_metadata.keys())

	response['results'] = users_with_metadata.values()

	for user in users_without_metadata:
		response['results'].append({"user": user})

	response['meta']['execution_time_seconds'] = time.time()-_start_time
	response['meta']['status'] = {'status':'OK','code':200, 'desc':''}

	if pretty:
		log.info(audit.message(request, response['meta']))
		return render_to_response('pretty_json.html', {'response': json.dumps(response, indent=2)})
	elif csv:
		output = '#' + json.dumps(response['meta'], indent=2).replace('\n','\n#') + '\n'
		output += array_to_csv(response['results'], metadata_attributes + ["user"])
		return HttpResponse(output, content_type="text/plain; charset=utf-8", status=response['meta']['status']['code'])
	else:
		log.info(audit.message(request, response['meta']))
		return HttpResponse(json.dumps(response), content_type="application/json", status=response['meta']['status']['code'])


