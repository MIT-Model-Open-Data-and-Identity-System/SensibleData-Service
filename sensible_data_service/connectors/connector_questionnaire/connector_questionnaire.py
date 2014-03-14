from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from authorization_manager import authorization_manager
import json
from utils.database import Database
import urllib
from accounts.models import UserRole
from backup import backup
import time
from django.utils.http import urlunquote
import pymongo
from utils import db_wrapper

def upload(request):

	auth = authorization_manager.authenticate_token(request, 'connector_questionnaire.input_form_data')
	if 'error' in auth:
		return HttpResponse(json.dumps(auth), status=401)

	user = auth['user']

	roles = None
	try: roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
	except: pass

	doc = urllib.unquote(request.REQUEST.get('doc'))
	doc = json.loads(doc)
	doc['user'] = user.username

	probe = 'dk_dtu_compute_questionnaire'

	backup.backupValue(data=doc, probe=probe, user=user.username)

	database_helper = db_wrapper.DatabaseHelper()
	try: doc_id = database_helper.insert(doc, collection=probe, roles=roles)
	except pymongo.errors.DuplicateKeyError: doc_id = '00'

	return HttpResponse(json.dumps({'ok':str(doc_id)}), status=200)

@csrf_exempt
def install(request):
	#return HttpResponse(urlunquote(request.POST))
	#return HttpResponse(request.POST.dict())	
	doc = json.loads(request.POST.get('data'))
	doc['timestamp_added'] = int(time.time())
	database = Database()
	probe = 'dk_dtu_compute_questionnaire_survey'
	doc_id = database.insert(doc, collection = probe)
	return HttpResponse(json.dumps({'ok':str(doc_id)}), status = 200)
