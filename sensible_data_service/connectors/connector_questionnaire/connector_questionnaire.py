from django.http import HttpResponse
from authorization_manager import authorization_manager
import json
from utils.database import Database
import urllib
from accounts.models import UserRole

def upload(request):

	auth = authorization_manager.authenticate_token(request, 'connector_questionnaire.input_form_data')
	if 'error' in auth:
		return HttpResponse(json.dumps(auth), status=401)

	user = auth['user']

	roles = None
	try: roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
	except: pass

	database = Database()
	doc = urllib.unquote(request.REQUEST.get('doc'))
	doc = json.loads(doc)
	doc['user'] = user.username
	doc_id = database.insert(doc, collection='dk_dtu_compute_questionnaire', roles=roles)

	return HttpResponse(json.dumps({'ok':str(doc_id)}), status=200)
