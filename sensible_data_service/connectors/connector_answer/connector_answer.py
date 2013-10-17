from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
from django.conf import settings
from .models import *

from authorization_manager import authorization_manager

def endpoint(request, answer):

	accepted_scopes = []

	try:
		for a in ConnectorAnswerEndpoint.objects.filter(active=True): 
			if answer.split('/')[0] == a.question and answer.split('/')[1] == a.answer:
				accepted_scopes = [x.scope for x in a.scopes.all()]
				exec('from questions.available_questions import '+a.question)
				method = eval(a.question+'.'+a.answer)
	except:
		response = {"error":"no such answer installed"}
		return HttpResponse(json.dumps(response), status=401, content_type="application/json")

	if len(accepted_scopes) == 0:
		response = {"error":"no such answer installed or is not configured properly"}
		return HttpResponse(json.dumps(response), status=401, content_type="application/json")


	auth = authorization_manager.authenticate_token(request)

	if 'error' in auth:
		response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
		return HttpResponse(json.dumps(response), status=401, content_type="application/json")
	
	auth_scopes = set([x for x in auth['scope']])

	if len(set(accepted_scopes) & auth_scopes) == 0:
		response = {'meta':{'status':{'status':'error','code':401,'desc':'token not authorized for any accepted scope %s'%str(list(accepted_scopes))}}}
		return HttpResponse(json.dumps(response), status=401, content_type="application/json")



	is_researcher = False
	for s in auth_scopes:
		#TODO or any of the accepted 'researcher' scopes
		if s == 'connector_raw.all_data_researcher': is_researcher = True
	
	users_to_return = buildUsersToReturn(auth['user'], request, is_researcher = is_researcher)

	user_roles = []
	try: user_roles = [x.role for x in UserRole.objects.get(user=auth['user']).roles.all()]
	except: pass

	own_data = False
	if len(users_to_return) == 1 and users_to_return[0] == auth['user'].username: own_data = True

	response = method(request=request, user=auth['user'], scopes=auth_scopes, users_to_return=users_to_return, user_roles=user_roles, own_data = own_data)


	if booleanize(request.GET.get('pretty', None)):
		return render_to_response('pretty_json.html', {'response': json.dumps(response, indent=2)})

	return HttpResponse(json.dumps(response), status=200, content_type="application/json")



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

def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	if string == 'true': return True
	return False
