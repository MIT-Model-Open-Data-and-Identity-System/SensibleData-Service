import base64
import calendar
from django.http import HttpResponse
import bson.json_util as json
from authorization_manager import authorization_manager
from sensible_audit import audit
from utils import db_wrapper
from django.shortcuts import render_to_response
from accounts.models import UserRole
from django.contrib.auth.models import User
import re
import urllib
import time
import transform
from connector_utils import *
from anonymizer.anonymizer import Anonymizer
from collections import OrderedDict
from connectors.connector_funf import device_inventory

"""
This is the MySQL specific version of connector_raw data getter.
It merges the phone_data and facebook_data
"""



log = audit.getLogger(__name__)

def wifi(request):
	return get_data(request, PHONE_DATA_SETTINGS['wifi'])
def bluetooth(request):
	return get_data(request, PHONE_DATA_SETTINGS['bluetooth'])
def location(request):
	return get_data(request, PHONE_DATA_SETTINGS['location'])
def calllog(request):
	return get_data(request, PHONE_DATA_SETTINGS['calllog'])
def sms(request):
	return get_data(request, PHONE_DATA_SETTINGS['sms'])
def questionnaire(request):
	return get_data(request,QUESTIONNAIRE_DATA_SETTINGS['questionnaire'])
def experience_sampling(request):
	return get_data(request, PHONE_DATA_SETTINGS['experience_sampling'])
def birthday(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['birthday'])
def education(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['education'])
def likes(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['likes'])
def friends(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['friends'])
def friendlists(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['friendlists'])
def groups(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['groups'])
def hometown(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['hometown'])
def interests(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['interests'])
def locationfacebook(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['locationfacebook'])
def political(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['political'])
def religion(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['religion'])
def work(request):
	return get_data(request, FACEBOOK_DATA_SETTINGS['work'])
def statuses(request):
        return get_data(request, FACEBOOK_DATA_SETTINGS['statuses'])
def feed(request):
        return get_data(request, FACEBOOK_DATA_SETTINGS['feed'])

def get_data(request, probe_settings):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))

	if decrypted:
		accepted_scopes = set([probe_settings['scope'], 'connector_raw.all_data'])
	else:
		accepted_scopes = set([probe_settings['scope'], 'connector_raw.all_data', 'connector_raw.all_data_researcher'])

	auth = authorization_manager.authenticate_token(request)

	if 'error' in auth:
		response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
		log.error(audit.message(request, response))
		return HttpResponse(json.dumps(response), status=401, content_type="application/json")

	auth_scopes = set([x for x in auth['scope']])

	if len(accepted_scopes & auth_scopes) == 0:
		response = {'meta':{'status':{'status':'error','code':401,'desc':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}}}
		log.error(audit.message(request, response))
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
	return dataBuild(request, probe_settings, users_to_return, decrypted = decrypted, own_data = own_data, roles = roles)
		

def dataBuild(request, probe_settings, users_to_return, decrypted = False, own_data = False, roles = None):
	if roles == None:
		roles = []
	_start_time = time.time()
	
	results = None
	query = None
	proc_req = None
	response = {}
	response['meta'] = {}

	try:
		if not users_to_return:
			raise BadRequestException('error',403,'The current token does not allow to view data from any users')
		proc_req = processApiCall(request, probe_settings, users_to_return)
		roles_to_use = []
                if own_data and 'researcher' in roles: roles_to_use = ['researcher']
                if own_data and 'developer' in roles: roles_to_use = ['developer']
		
		try:
			db = db_wrapper.DatabaseHelper()
			docs = db.retrieve(proc_req, probe_settings['collection'], roles_to_use)
			#raise BadRequestException('error',200,json.dumps({'proc_req':proc_req,'probe_settings':probe_settings['collection'],'roles':roles}))
			results = cursorToArray(docs, decrypted = decrypted,\
					probe=probe_settings['collection'],\
					is_researcher = ('researcher' in roles),\
					map_to_users=proc_req['map_to_users'])
		except Exception as e:
			raise BadRequestException('error',500,'The request caused a DB malfunction: ' + str(e))
		results_count = len(results)

		response['meta']['status'] = {'status':'success','code':200}
		response['meta']['results_count'] = len(results)
		response['meta']['api_call'] = proc_req 
		response['meta']['query'] = query
		response['results'] = results

		if len(results) > 0:
			if results_count == proc_req['limit']:
				response['meta']['paging'] = {}
				response['meta']['paging']['cursors'] = {}

				if proc_req['after'] is not None:
					response['meta']['paging']['cursors']['after'] = str(int(proc_req['after']) + 1)
					response['meta']['paging']['links'] =\
						{'next':re.sub('&after=[^ &]+','&after=' + str(response['meta']['paging']['cursors']['after']),request.build_absolute_uri())}
				else:
					response['meta']['paging']['links'] = \
						{'next':request.build_absolute_uri() + '&after=' + str(1)}
	except BadRequestException as e:
		response['meta']['status'] = e.value
		proc_req = {'format':'json'}
	
	response['meta']['execution_time_seconds'] = time.time()-_start_time
	callback = request.REQUEST.get('callback','')

	if len(callback) > 0:
		data = '%s(%s);' % (callback, json.dumps(response))
		return HttpResponse(data, content_type="text/javascript", status=response['meta']['status']['code'])

	if decrypted:
		pass
	

	# users_return=[]
	# users_results = cursorToArray(results, decrypted = decrypted, probe=probe_settings['collection'])
	# for data_users in users_results:
	# 	if data_users['user'] not in users_return:
	# 		users_return.append(data_users['user'])
	
	if proc_req['format'] == 'pretty':
		return render_to_response('pretty_json.html', {'response': json.dumps(response, indent=2)})
        elif proc_req['format'] == 'csv':
		output = '#' + json.dumps(response['meta'], indent=2).replace('\n','\n#') + '\n'
		output += array_to_csv(results)
		return HttpResponse(output, content_type="text/plain", status=response['meta']['status']['code'])
	else:
		return HttpResponse(json.dumps(response), content_type="application/json", status=response['meta']['status']['code'])
	return HttpResponse('hello decrypted')


def array_to_csv(results):
	if not results: return ''
	fields = results[0].keys()
	output = [','.join(fields)]
	for result in results:
		output.append(','.join([str(result[k]) for k in fields]))
	return '\n'.join(output)
		


def cursorToArray(cursor, decrypted = False, probe = '', is_researcher=False, map_to_users=False):
	array = []
	for row in cursor:
		if 'timestamp' in row:
			row['timestamp'] = int(calendar.timegm(row['timestamp'].timetuple()))
		if 'timestamp_added' in row:
			row['timestamp_added'] = int(calendar.timegm(row['timestamp_added'].timetuple()))
		array.append(row)

	if 'ExperienceSamplingProbe' in probe:
		anonymizer = Anonymizer()
		for doc in array:
			doc['answer'] = json.loads(base64.b64decode(doc['answer']))
			anonymizer.anonymizeDocument(doc, probe)


	if 'BluetoothProbe' not in probe: return array
	if decrypted:
		anonymizer = Anonymizer()
		return anonymizer.deanonymizeDocument(array, probe)
	if is_researcher and map_to_users:
		deviceInventory = device_inventory.DeviceInventory()
		for doc in array:
			try:
				user_temp = deviceInventory.mapBtToUser(doc['bt_mac'], doc['timestamp'], use_mac_if_empty=False)
				if user_temp is not None:
					doc['scanned_user'] = user_temp
				else:
					doc['scanned_user'] = ''
			except KeyError: doc['scanned_user'] = ''
	return array

def buildUsersToReturn(auth_user, request, is_researcher = False):
	users_to_return = []
	if not is_researcher:
		users_to_return.append(auth_user.username)
		return users_to_return
	
	requested_users = [user for user in request.REQUEST.get('users','').split(',') if len(user) > 0]
	if len(requested_users) > 0:
		users_to_return = requested_users
	else: users_to_return.append('all')
	return users_to_return

def processApiCall(request, probe_settings, users_to_return):
	
	response = {}
	api_params = ['bearer_token','sortby','decrypted','order','fields','start_date','end_date','limit','users','after','callback', 'format', 'map_to_users', 'questions', 'form_version']
	for k in request.REQUEST.keys():
		if k not in api_params:
			raise BadRequestException('error',400, str(k) + ' is not a legal API parameter.'\
					+' Legal API parameters are: ' + ', '.join(api_params))

	response['fields'] = None
	response['sortby'] = None
	response['order'] = None
	response['start_date'] = None
	response['end_date'] = None
	response['limit'] = 1000
	response['users'] = None
	response['after'] = None
	response['format'] = 'json'
	response['map_to_users'] = False
	response['where'] = {}

	### deal with sorting
	# sorting will be supported later. Now, we can only sort by data.TIMESTAMP, either asc or desc
	response['sortby'] = 'timestamp'
	if request.REQUEST.get('order', None) is not None:
		if request.REQUEST.get('order',None) not in ['-1','1']:
			raise BadRequestException('error',400,str(request.REQUEST.get('order')) + ' is not a valid value for order parameter. Use 1 for ascending or -1 for descending')
		else:
			response['order'] = int(request.REQUEST.get('order'))
	else:
		response['order'] = -1
	
	### deal with fields
	fields_string = request.REQUEST.get('fields', '')
	print fields_string
	if len(fields_string) > 0:
		response['fields'] = ['id', 'user', 'timestamp']
		response['fields'] += [field for field in fields_string.split(',') if len(field) > 0 and field != 'sensible_token']
		print response['fields']
	# default set of fields
	else:
		response['fields'] = set(probe_settings['default_fields'])
		
	### deal with start_date and end_date
	if request.REQUEST.get('start_date',None) is not None:
		try:
			response['start_date'] = int(request.REQUEST.get('start_date'))
		except ValueError:
			raise BadRequestException('error',400,request.REQUEST.get('start_date') + ' is not a valid value for the start_date parameter. Use an integer value')
	if request.REQUEST.get('end_date',None) is not None:
		try:
			response['end_date'] = int(request.REQUEST.get('end_date'))
		except:
			raise BadRequestException('error',400,request.REQUEST.get('end_date') + ' is not a valid value for the end_date parameter. Use an integer value')

	### deal with limit
	if int(request.REQUEST.get('limit',1000)) < 1000:
		try:
			response['limit'] = int(request.REQUEST.get('limit'))
		except ValueError:
			raise BadRequestException('error',400, request.REQUEST.get('limit') + ' is not a valid value for the limit parameter. Use an integer value')
	
	# list of users is passed as function argument	
	response['users'] = users_to_return
	
	### deal with after (paging)
	if request.REQUEST.get('after', None) is not None:
		response['after'] = request.REQUEST.get('after', None)
	
	### deal with format
	if request.REQUEST.get('format',None) is not None:
		if request.REQUEST.get('format',None) not in ['pretty','json','csv']:
			raise BadRequestException('error',400,str(request.REQUEST.get('format',None)) + ' is not a valid format. Valid formats are: pretty, json, csv')
		else:
			response['format'] = request.REQUEST.get('format',None)
	
	### deal with map_to_users
	if request.REQUEST.get('map_to_users',None) is not None:
		if request.REQUEST.get('map_to_users', None) not in ['1','0']: 
			raise BadRequestException('error',400,str(request.REQUEST.get('map_to_users',None)) + ' is not a valid value for map_to_users. Valid values are \'0\' and \'1\'')
		else:
			if request.REQUEST.get('map_to_users',None) == '1':
				response['map_to_users'] = True
	#deal with questionnaire queries
	questionnaire_questions = request.REQUEST.get("questions")
	if questionnaire_questions:
		response["where"]["variable_name"] = [question for question in questionnaire_questions.split(",") if len(question) > 0]
	questionnaire_form_version = request.REQUEST.get("form_version")
	if questionnaire_form_version:
		response["where"]["form_version"] = [questionnaire_form_version]

	### return
	response['bearer_token'] = request.REQUEST.get('bearer_token')
	return response


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
