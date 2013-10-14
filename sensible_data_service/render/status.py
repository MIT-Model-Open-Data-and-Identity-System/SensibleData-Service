from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
import bson.json_util as json
from utils import database
from django.contrib.auth.models import User
from documents.models import InformedConsent
from django.conf import settings
import pymongo
from sensible_data_service import settings as service_settings

@login_required
def status(request):
	authorized_users = ['arks@dtu.dk', 'sljo@dtu.dk', 'lasse.valentini@gmail.com']
	if not request.user.email in authorized_users:
		return HttpResponse(json.dumps({'error':'sorry, %s you are not authorized :('%request.user.username}))
	query = request.REQUEST.get('query', '')
	if query == '':
		return render_to_response('status.html', {'api_uri':settings.BASE_URL+'status/', 'service_name':service_settings.SERVICE_NAME}, context_instance=RequestContext(request))
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
	try:
		db = database.Database()
		values['documents_no'] = db.getDocuments(query={}, collection='dk_dtu_compute_questionnaire').count()
		values['users'] = len(db.getDocuments(query={}, collection='dk_dtu_compute_questionnaire').distinct('user'))
		values['finished'] = db.getDocuments(query={'variable_name':'_submitted'}, collection='dk_dtu_compute_questionnaire').count()
		values['male'] = db.getDocuments(query={'variable_name':'sex', 'response':'mand'}, collection='dk_dtu_compute_questionnaire').count()
		values['female'] = db.getDocuments(query={'variable_name':'sex', 'response':'kvinde'}, collection='dk_dtu_compute_questionnaire').count()
	except: pass
	return HttpResponse(json.dumps(values))

def facebook_request(request):
	values = {}
	sections = ['birthday','education','feed','friendlists','friendrequests','friends','groups','hometown','interests','likes','location','locations','political','religion','statuses','work']
	try:
		db = database.Database()
		for x in sections:
			values[x+'_doc'] = db.getDocuments(query={}, collection='dk_dtu_compute_facebook_'+x).count()
			values[x+'_users'] = len(db.getDocuments(query={}, collection='dk_dtu_compute_facebook_'+x).distinct('user'))
	except: pass
	return HttpResponse(json.dumps(values))

def mobile_request(request):
	values = {}
	sections =['BluetoothProbe','CallLogProbe','CellProbe','ContactProbe','HardwareInfoProbe','LocationProbe','ScreenProbe','SMSProbe','TimeOffsetProbe','WifiProbe']
	try:
		db = database.Database()
		for x in sections:
			values[x+'_doc'] = db.getDocuments(query={}, collection = 'edu_mit_media_funf_probe_builtin_'+x).count()
			values[x+'_users'] = db.getDocuments(query={}, collection='statistics_question_edu_mit_media_funf_probe_builtin_'+x).count()
	except: pass
	return HttpResponse(json.dumps(values))

def getDatabaseStatus():
	try:
		db = database.Database()
		doc_id = db.insert({'test':'test'}, 'test')
		response = db.db['test'].remove({'_id':doc_id})
		if response['ok'] == 1:
			return 'OK'
		else:
			return response
	except pymongo.errors.PyMongoError as e: return str(e)


def getDatabaseStats():
	try:
		db = database.Database()
		return db.db.command('dbstats')
	except pymongo.errors.PyMongoError: return {'error': 'something went terribly wrong'}
