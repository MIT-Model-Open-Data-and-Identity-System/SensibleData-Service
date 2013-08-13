from django.http import HttpResponse
import bson.json_util as json
from authorization_manager import authorization_manager
from utils import database
from django.shortcuts import render_to_response

def questionnaire(request):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))

	if decrypted:
		return questionnaireDecrypted(request)
	else:
		return questionnaireEncrypted(request)






def questionnaireDecrypted(request):

	accepted_scopes = set(['connector_raw.all_data', 'connector_raw.all_data_encrypted'])

	auth = authorization_manager.authenticate_token(request)
	if 'error' in auth:
		return HttpResponse(json.dumps(auth), status=401)
	
	auth_scopes = set([x for x in auth['scope']])

	if len(accepted_scopes & auth_scopes) == 0:
		return HttpResponse(json.dumps({'error':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}), status=401)


	#TODO: researcher token: valid for every user, should have researcher user attached to it

	#TODO: parameters: user (if can be any), time, etc.

	db = database.Database()
	docs = db.getDocuments(query={}, collection='dk_dtu_compute_questionnaire_researcher')

	pretty = booleanize(request.REQUEST.get('pretty', False))

	if pretty:
		return render_to_response('pretty_json.html', {'response': json.dumps(docs, indent=2)})
	else:
		return HttpResponse(json.dumps(docs))

def questionnaireEncrypted(request):
	return HttpResponse('hello')


def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	return False
