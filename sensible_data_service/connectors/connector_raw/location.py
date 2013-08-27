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
	accepted_scopes = set(['connector_raw.location', 'connector_raw.all_data'])

	auth = authorization_manager.authenticate_token(request)
	if 'error' in auth:
		return HttpResponse(json.dumps(auth), status=401)

	auth_scopes = set([x for x in auth['scope']])

	if len(accepted_scopes & auth_scopes) == 0:
		return HttpResponse(json.dumps({'error':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}), status=401)

	if ('dummy' in request.REQUEST.keys()):
		return HttpResponse('[]', content_type="application/json")
	users_to_return = buildUsersToReturn(auth['user'], request)
	
	#(fields, sort, start_date, end_date) = processApiCall(request)
	proc_req = processApiCall(request)
	
	# response field only set if there was an error in the api call, return the description
	if proc_req['response']:
		return proc_req['response']
	query = buildQuery(users_to_return, proc_req['start_date'], proc_req['end_date'])	
	collection = 'edu_mit_media_funf_probe_builtin_LocationProbe_researcher'
	
	
	db = database.Database()
	docs = db.getDocumentsCustom(query=query, collection=collection, fields = proc_req['fields'])
	if proc_req['sortby'] is not None:
		docs = docs.sort(proc_req['sortby'], proc_req['order'])
	#@ FIXME <deprecated>
	else:
		if proc_req['sort'] in [-1, 1]:
			docs = docs.sort("timestamp", proc_req['sort'])
	#@ FIXME </deprecated>
	pretty = booleanize(request.REQUEST.get('pretty', False))
	if pretty:
		return render_to_response('pretty_json.html', {'response': json.dumps(docs, indent=2)})
	else:
		return HttpResponse(json.dumps(docs), content_type="application/json")
	return HttpResponse('hello decrypted')


def buildUsersToReturn(auth_user, request):
	users_to_return = []
	roles = []
	users_to_return.append(auth_user.username)
	#FIXME remove
	users_to_return.append('cb88b9866e4aed333114166c0f0a4b')
	return users_to_return

def processApiCall(request):
	response = {}
	response['response'] = None
	response['fields'] = None
	response['sortby'] = None
	response['order'] = None
	#@ FIXME<deprecated>
	response['sort'] = None
	#@ FIXME</deprecated>
	response['start_date'] = None
	response['end_date'] = None
	response['limit'] = 1000
	
	### deal with fields
	fields_string = request.REQUEST.get('fields', '')
	if len(fields_string) > 0:
		response['fields'] = {}
		for field in fields_string.split(','):
			response['fields'][field] = 1
	# default set of fields
	else:
		response['fields'] = {\
				'timestamp':1,\
				'_id':0,\
				'data.LOCATION.geojson.coordinates':1,\
				'data.LOCATION.mProvider':1,\
				'data.LOCATION.mAccuracy':1}

	### deal with sorting
	sortby = request.REQUEST.get('sortby',None)
	if sortby is not None:
		response['sortby'] = sortby
		order = request.REQUEST.get('order',None)
		if order is not None:
			if int(order) in [-1, 1]:
				response['order'] = int(order)
			else:
				response['response'] = HttpResponse(order + ' is not a valid value for oder param. Use 1 for ascending or -1 for descending')
				return response
		else:
			response['response'] = HttpResponse('You have to specify the order using the order param. Use 1 for ascending or -1 for descending')
	else:
		#@ FIXME <deprecated>
		sort = request.REQUEST.get('sort',None)
		if sort is not None:
			if int(sort) not in [-1, 1]:
				return HttpResponse(sort + ' is not a valid value for sort param. Use 1 for ascending or -1 for descending')
			else:
				response['sort'] = int(sort)
		#@ FIXME </deprecated>

	
	
	### deal with start_date and end_date
	if request.REQUEST.get('start_date',None) is not None:
		response['start_date'] = int(request.REQUEST.get('start_date'))
	if request.REQUEST.get('end_date',None) is not None:
		response['end_date'] = int(request.REQUEST.get('end_date'))

	### deal with limit
	if request.REQUEST.get('limit',1000) < 1000:
		response['limit'] = request.REQUEST.get('limit')
	return response


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
	if string == 'true': return True
	return False
