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

def location(request):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))

	if decrypted:
		accepted_scopes = set(['connector_raw.location', 'connector_raw.all_data'])
	else:
		accepted_scopes = set(['connector_raw.location', 'connector_raw.all_data', 'connector_raw.all_data_researcher'])

	auth = authorization_manager.authenticate_token(request)

	if 'error' in auth:
		response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
		return HttpResponse(json.dumps(response), status=401, content_type="application/json")

	auth_scopes = set([x for x in auth['scope']])

	if len(accepted_scopes & auth_scopes) == 0:
		response = {'meta':{'status':{'status':'error','code':401,'desc':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}}}
		return HttpResponse(json.dumps(response), status=401)
	
	if ('dummy' in request.REQUEST.keys()):
		return HttpResponse('[]', content_type="application/json")

	is_researcher = False
	for s in auth_scopes:
		if s == 'connector_raw.all_data_researcher': is_researcher = True

	users_to_return = buildUsersToReturn(auth['user'], request, is_researcher = is_researcher)
	roles = []
	try: roles = [x.role for x in UserRole.objects.get(user=auth['user']).roles.all()]
	except: pass

	own_data = False
	if len(users_to_return) == 1 and users_to_return[0] == auth['user'].username: own_data = True


	return locationBuild(request, users_to_return, decrypted = decrypted, own_data = own_data, roles = roles)

def locationBuild(request, users_to_return, decrypted = False, own_data = False, roles = []):
	_start_time = time.time()
	
	pretty = booleanize(request.REQUEST.get('pretty', False))
	results = None
	query = None
	proc_req = None
	response = {}
	response['meta'] = {}

	try:
		if len(users_to_return) == 0:
			raise BadRequestException('error',403,'The current token does not allow to view data from any users')
		proc_req = processApiCall(request, users_to_return)
		query = buildQuery(users_to_return, proc_req)	
		collection = 'edu_mit_media_funf_probe_builtin_LocationProbe'
		if own_data and 'researcher' in roles: collection += '_researcher'

		
		db = database.Database()
	#Let's not build indexes like that, this may be very ineficcient (blocking index building, no control over space); we also should NOT build indexes in background, bad experience with data consistency

#		if proc_req['sortby'] is None:
#		db.db[collection].ensure_index([('data.TIMESTAMP',-1),('_id',1)])
#		db.db[collection].ensure_index([('data.TIMESTAMP',1),('_id',1)])
#		db.db[collection].ensure_index([('user',1),('_id',1)])
#		else:
#			db.db[collection].ensure_index([(proc_req['sortby'],proc_req['order']), ('_id',1)])
		
		docs = db.getDocumentsCustom(query=query, collection=collection,\
				fields = proc_req['fields'])

		### hinting
		# if the users are specified, we use the hint with users
		if proc_req['users'] is not None:
			docs = docs.hint([('data.TIMESTAMP',proc_req['order']), ('_id',1), ('user',1)])
		# else, we use only id and timestamp
		else:
			docs = docs.hint([('data.TIMESTAMP',proc_req['order']), ('_id',1)])
		#pagination (skipping)
		if proc_req['after'] is not None:
			docs = docs.skip(1)

		#apply limit
		docs.limit(proc_req['limit'])

		try:
			results = cursorToArray(docs)
		except Exception as e:
			raise BadRequestException('error',500,'The request caused a DB malfunction: ' + str(e))
		results_count = len(results)

		response['meta']['status'] = proc_req['status']
		response['meta']['results_count'] = len(results)
		response['meta']['api_call'] = request.REQUEST
		response['meta']['query'] = query
		response['results'] = results

		if len(results) > 0:
			response['meta']['paging'] = {}
			response['meta']['paging']['cursors'] = {}
			response['meta']['paging']['cursors']['after'] =\
					{proc_req['sortby']:getValueOfFullKey(results[-1], proc_req['sortby']),\
					'_id':results[-1]['_id'],
					'user':results[-1]['user']}
			if results_count == proc_req['limit']:
				if proc_req['after'] is not None:	
					response['meta']['paging']['links'] =\
						{'next':re.sub('&after=[^ &]+','&after=' + urlize_dict(response['meta']['paging']['cursors']['after']),request.build_absolute_uri())}
				else:
					response['meta']['paging']['links'] = \
						{'next':request.build_absolute_uri() + '&after=' + urlize_dict(response['meta']['paging']['cursors']['after'])}
	except BadRequestException as e:
		response['meta']['status'] = e.value
	
	response['meta']['execution_time_seconds'] = time.time()-_start_time
	callback = request.REQUEST.get('callback','')

	if len(callback) > 0:
		data = '%s(%s);' % (callback, json.dumps(response))
		return HttpResponse(data, content_type="text/javascript", status=response['meta']['status']['code'])

	if decrypted:
		pass

	if pretty:
		return render_to_response('pretty_json.html', {'response': json.dumps(response, indent=2)})
	else:
		return HttpResponse(json.dumps(response), content_type="application/json", status=response['meta']['status']['code'])
	return HttpResponse('hello decrypted')

def urlize_dict(dictionary):
	return urllib.quote(json.dumps(dictionary, indent=None, separators=(',',':')))


def cursorToArray(cursor):
	return [doc for doc in cursor]

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


	return users_to_return

def processApiCall(request, users_to_return):
	
	response = {}
	api_params = ['bearer_token','pretty','decrypted','sortby','order','fields','start_date','end_date','limit','users','after','sort', 'callback']
	for k in request.REQUEST.keys():
		if k not in api_params:
			raise BadRequestException('error',400, str(k) + ' is not a legal API parameter.'\
					+' Legal API parameters are: ' + ', '.join(api_params))

	response['status'] = {'status':'OK','code':200, 'desc':''}
	response['fields'] = None
	response['sortby'] = None
	response['order'] = None
	#@ FIXME<deprecated>
	response['sort'] = None
	#@ FIXME</deprecated>
	response['start_date'] = None
	response['end_date'] = None
	response['limit'] = 1000
	response['users'] = None
	response['after'] = None

	### deal with sorting
	# sorting will be supported lated. Now, we can only sort by data.TIMESTAMP, either asc or desc
	response['sortby'] = 'data.TIMESTAMP'
	if request.REQUEST.get('order', None) is not None:
		if request.REQUEST.get('order',None) not in ['-1','1']:
			raise BadRequestException('error',400,str(request.REQUEST.get('order')) + ' is not a valid value for order parameter. Use 1 for ascending or -1 for descending')
		else:
			response['order'] = int(request.REQUEST.get('order'))
	elif request.REQUEST.get('sort', None) is not None:
		if request.REQUEST.get('sort',None) not in ['-1','1']:
			raise BadRequestException('error',400,str(request.REQUEST.get('sort')) + ' is not a valid value for order parameter. Use 1 for ascending or -1 for descending')
		else:
			response['order'] = int(request.REQUEST.get('sort'))
	else:
		response['order'] = -1
#	sortby = request.REQUEST.get('sortby',None)
#	if sortby is not None:
#		response['sortby'] = sortby
#		order = request.REQUEST.get('order',None)
#		if order is not None:
#			if order in ['-1', '1']:
#				response['order'] = int(order)
#			else:
#				raise BadRequestException('error',400,str(order) + ' is not a valid value for order parameter. Use 1 for ascending or -1 for descending')
#		else:
#			raise BadRequestException('error',400,'You have to specify the order of sorting. Use 1 for ascending or -1 for descending')
#	else:
#		#@ FIXME <deprecated>
#		sort = request.REQUEST.get('sort',None)
#		if sort is not None:
#			if sort not in ['-1', '1']:
#				raise BadRequestException('error',400,str(sort) + ' is not a valid value for order parameter. Use 1 for ascending or -1 for descending')
#			else:
#				response['sortby'] = 'data.TIMESTAMP'
#				response['order'] = int(sort)
#		#@ FIXME </deprecated>
#		else:
#			response['sortby'] = 'data.TIMESTAMP'
#			if request.REQUEST.get('order',None) is not None:
#				if request.REQUEST.get('order',None) in ['-1','1']:
#					response['order'] = int(request.REQUEST.get('order',None))
#				else:
#					raise BadRequestException('error',400,str(request.REQUEST.get('order')) + ' is not a valid value for order parameter. Use 1 for ascending or -1 for descending')	
#			else:
#				response['order'] = -1
	
	### deal with fields
	fields_string = request.REQUEST.get('fields', '')
	if len(fields_string) > 0:
		response['fields'] = {\
                                'user':1,\
                                'data.TIMESTAMP':1,\
                                '_id':1}
		for field in fields_string.split(','):
			if len(field) > 0 and field != 'sensible_token':
				response['fields'][field] = 1
		response['fields']['_id'] = 1
	# default set of fields
	else:
		response['fields'] = {\
				'user':1,\
				'data.TIMESTAMP':1,\
				'_id':1,\
				'data.LOCATION.geojson.coordinates':1,\
				'data.LOCATION.mProvider':1,\
				'data.LOCATION.mAccuracy':1}
	# always add the field by which sorting is done
	if response['sortby'] not in response['fields'].keys():
		response['fields'][response['sortby']] = 1

		
	### deal with start_date and end_date
	if request.REQUEST.get('start_date',None) is not None:
		response['start_date'] = int(request.REQUEST.get('start_date'))
	if request.REQUEST.get('end_date',None) is not None:
		response['end_date'] = int(request.REQUEST.get('end_date'))

	### deal with limit
	if int(request.REQUEST.get('limit',1000)) < 1000:
		response['limit'] = int(request.REQUEST.get('limit'))
	
	### deal with the list of users
	#if request.REQUEST.get('users', None) is not None:
	#	response['users'] = [user for user in request.REQUEST.get('users').split(',') if len(user) > 0]
	response['users'] = users_to_return
	
	### deal with after/before
	if request.REQUEST.get('after', None) is not None:

		response['after'] = json.loads(request.REQUEST.get('after', None))

	### return
	return response


def buildQuery(users_to_return, request):
	query = {'$query':{}}
	if not 'all' in users_to_return:
		query['$query']['user'] = {'$in':users_to_return}
	

#	if request['after'] is not None:
#		query['_id'] = {}
#		query['_id']['&gt'] = request['after']['_id']
#	elif request['before'] is not None:
#		query['_id'] = {}
#		query['_id']['&lt'] = request['before']['_id']
	
	
	if request['after'] is not None: # there is paging involved
		#if request['order']==1:
		query['$min'] = request['after']
		#else:
		#	query['$max'] = request['after']

	#query['$hint'] = {str(request['sortby']) : request['order'], '_id':1}
	
	if request['end_date'] is not None or request['start_date'] is not None:
		query['$query']['data.TIMESTAMP'] = {}
		if request['end_date'] is not None:
			query['$query']['data.TIMESTAMP']['$lte'] = request['end_date']
		if request['start_date'] is not None:
			query['$query']['data.TIMESTAMP']['$gte'] = request['start_date']
		
	return query



def getValueOfFullKey(dictionary, fullkey):
	result = dictionary
	for key in fullkey.split('.'):
		result = result[key]
	return result

class BadRequestException(Exception):
	def __init__(self, value):
		self.value = value
	
	def __init__(self, status, code, description):
		self.value = {}
		self.value['status'] = status
		self.value['code'] = code
		self.value['desc'] = description
	
	def __str__(self):
		return repr(self.value)
