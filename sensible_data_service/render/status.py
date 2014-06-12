from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import bson.json_util as json
from db_access.named_queries import NAMED_QUERIES
from django.contrib.auth.models import User
from documents.models import InformedConsent
from django.conf import settings
from utils import db_wrapper, SECURE_settings, database
import pymongo

@login_required
def status(request):
	authorized_users = SECURE_settings.AUTHORIZED_STATUS_VIEWERS#['arks@dtu.dk', 'sljo@dtu.dk', 'lasse.valentini@gmail.com', "radu.gatej@gmail.com"]
	if not request.user.email in authorized_users:
		return HttpResponse(json.dumps({'error':'sorry, %s you are not authorized :('%request.user.username}))
	query = request.REQUEST.get('query', '')
	if query == '':
		return render_to_response('status.html', {'api_uri':settings.BASE_URL+'status/'}, context_instance=RequestContext(request))
	if query =='users':
		return users_request(request)
	if query =='database':
		return database_request(request)
	if query =='questionnaires':
		return questionnaires_request(request)
	if query =='facebook':
		return facebook_request(request)
	if query =='mobile':
		return mobile_request(request)

def users_request(request):
	values = {}
	values['users_no'] = User.objects.count()
	values['users_informed_consent_no'] = InformedConsent.objects.count()
	return HttpResponse(json.dumps(values))

def database_request(request):
	values = {}
	values['database_status'] = getDatabaseStatus()
	values['database_stats'] = getDatabaseStats()
	values['database_config'] = json.dumps(settings.DATA_DATABASE)
	return HttpResponse(json.dumps(values))

def questionnaires_request(request):
	values = {}
	#try:
	db = db_wrapper.DatabaseHelper()
	values['documents_no'] = db.retrieve({}, "dk_dtu_compute_questionnaire").rowcount
	values['users'] = db.execute_named_query(NAMED_QUERIES["count_unique_questionnaire_users"], None).fetchone().values()[0]
	values['finished'] = db.execute_named_query(NAMED_QUERIES["count_questionnaire_users_with_variable"], ("_submitted",)).fetchone().values()[0]
	values['male'] = db.execute_named_query(NAMED_QUERIES["count_questionnaire_users_by_sex"], ("mand",)).fetchone().values()[0]
	values['female'] = db.execute_named_query(NAMED_QUERIES["count_questionnaire_users_by_sex"], ("kvinde",)).fetchone().values()[0]
	#except: pass
	return HttpResponse(json.dumps(values))

def facebook_request(request):
	values = {}
	fb_data_types = ['birthday','education','feed','friendlists','friendrequests','friends','groups','hometown','interests','likes','location','locations','political','religion','statuses','work']
	db = db_wrapper.DatabaseHelper()
	for data_type in fb_data_types:
		values[data_type+'_doc'] = db.retrieve({}, 'dk_dtu_compute_facebook_' + data_type).rowcount
		values[data_type+'_users'] = db.execute_named_query(NAMED_QUERIES["count_unique_facebook_users"], (data_type,)).fetchone().values()[0]
	return HttpResponse(json.dumps(values))

def mobile_request(request):
	values = {}
	sections =['BluetoothProbe','CallLogProbe','CellProbe','ContactProbe','HardwareInfoProbe','LocationProbe','ScreenProbe','SMSProbe','TimeOffsetProbe','WifiProbe']
	try:
		db = db_wrapper.DatabaseHelper()
		for x in sections:
			values[x+'_doc'] = db.retrieve({}, 'edu_mit_media_funf_probe_builtin_'+x).rowcount
			count_funf_users_query = NAMED_QUERIES["count_funf_unique_users_by_probe"]
			count_funf_users_query["database"] = 'edu_mit_media_funf_probe_builtin_'+x
			values[x+'_users'] = db.execute_named_query(count_funf_users_query, None).fetchone().values()[0]
	except: pass
	return HttpResponse(json.dumps(values))

def getDatabaseStatus():
	try:
		db = database.Database()
		doc_id = db.insert({'test':'test'}, 'test')
		response = db.getDatabase('test')['test'].remove({'_id':doc_id})
		if response['ok'] == 1:
			return 'OK'
		else:
			return response
	except pymongo.errors.PyMongoError as e: return str(e)


def getDatabaseStats():
	try:
		db = database.Database()
		return_value = {}
		return_value[db.default_database] = db.getDatabase(db.default_database).command('dbstats')
		for d in db.available_databases:
			return_value[db.available_databases[d]] = db.getDatabase(d).command('dbstats')
		return return_value
	except pymongo.errors.PyMongoError: return {'error': 'something went terribly wrong'}
