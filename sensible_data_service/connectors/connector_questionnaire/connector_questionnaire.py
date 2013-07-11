from django.http import HttpResponse
from authorization_manager import authorization_manager
import json
from utils.database import Database
import urllib

def upload(request):

	auth = authorization_manager.authenticate_token(request)
	if 'error' in auth:
		return HttpResponse(json.dumps(auth), status=401)
	

	user = auth['user']
	database = Database()
	doc = urllib.unquote(request.REQUEST.get('doc'))
	doc = json.loads(doc)
	doc['user'] = user.username
	doc_id = database.insert(doc, collection='questionnaire')

	return HttpResponse(json.dumps({'ok':str(doc_id)}), status=200)
