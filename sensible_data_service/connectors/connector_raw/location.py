from django.http import HttpResponse
import bson.json_util as json
from authorization_manager import authorization_manager
from utils import database
from django.shortcuts import render_to_response
from accounts.models import UserRole
from django.contrib.auth.models import User

def location(request):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))

	if decrypted:
		return locationDecrypted(request)
	else:
		return locationEncrypted(request)

def locationDecrypted(request):
	accepted_scopes = set(['connector_raw.location'])

	auth = authorization_manager.authenticate_token(request)
	if 'error' in auth:
		return HttpResponse(json.dumps(auth), status=401)

	auth_scopes = set([x for x in auth['scope']])

	if len(accepted_scopes & auth_scopes) == 0:
		return HttpResponse(json.dumps({'error':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}), status=401)


	users_to_return = buildUsersToReturn(auth['user'], request)
	
	(fields, sort, start_date, end_date) = processApiCall(request)
	query = buildQuery(users_to_return, start_date, end_date)
	
	collection = 'edu_mit_media_funf_probe_builtin_LocationProbe'
	
	
	db = database.Database()
	docs = db.getDocumentsCustom(query=query, collection=collection, fields = fields)
	if sort in [-1, 1]:
		docs = docs.sort("timestamp",sort)

	pretty = booleanize(request.REQUEST.get('pretty', False))
	if pretty:
		return render_to_response('pretty_json.html', {'response': json.dumps(docs, indent=2)})
	else:
		return HttpResponse(json.dumps(docs), content_type="application/json")
	return HttpResponse('hello decrypted')


def buildUsersToReturn(auth_user, request):
	users_to_return = []
	roles = []
	try: roles = [x.role for x in UserRole.objects.get(user=auth_user).roles.all()]
	except: pass
	if 'researcher' in roles:
		users_to_return = [x.username for x in User.objects.filter().all()]
	else:
		users_to_return.append(auth_user.username)
	return users_to_return

def processApiCall(request):
	fields = None
	sort = None
	start_date = None
	end_date = None
	
	# deal with fields
	fields_string = request.REQUEST.get('fields', '')
	if len(fields_string) > 0:
		fields = {}
		for field in fields_string.split(','):
			fields[field] = 1
	
	# deal with sorting
	sort = request.REQUEST.get('sort',None)
	if sort is not None:
		if int(sort) not in [-1, 1]:
			return HttpResponse(sort + ' is not a valid value for sort param. Use 1 for ascending or -1 for descending')
		else:
			sort = int(sort)
	
	
	# deal with start_date and end_date
	if request.REQUEST.get('start_date',None) is not None:
		start_date = int(request.REQUEST.get('start_date'))
	if request.REQUEST.get('end_date',None) is not None:
		end_date = int(request.REQUEST.get('end_date'))

	return (fields, sort, start_date, end_date)


def buildQuery(users_to_return, start_date, end_date):
	query = {}
	query['user'] = {'$in':users_to_return}
	if start_date is not None or end_date is not None:
		query['timestamp'] = {}
		if start_date is not None:
			query['timestamp']['$gte'] = start_date
		if end_date is not None:
			query['timestamp']['$lt'] = end_date
	
	return query



def locationEncrypted(request):
	return HttpResponse('hello encrypted')


def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	return False
