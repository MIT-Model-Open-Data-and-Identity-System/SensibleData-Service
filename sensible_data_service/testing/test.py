from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from authorization_manager.authorization_manager import *
import bson.json_util as json
from connector_pipes.connector_pipe_funf import connector_pipe_funf
from application_manager.application_manager import ApplicationManager

def testing(request):
	authorizationManager = AuthorizationManager()


	user = 'arek'
	pipe = 'connector_funf'
	scope = 'input'
	params = {'token':'cde'}

	#authorizationManager.insertAuthorization(user, pipe, scope, params)
	#response = {'hello':'world'}

	pipe = connector_pipe_funf.ConnectorFunfPipe()

	applicationManager = ApplicationManager()
	response = applicationManager.registerApplication(name='krowa', owner='john', connector='connector_funf', scopes='all_probes', description="this is an awesome app", params={})

	#response = pipe.getAuthorization('aaaa')

	return HttpResponse(json.dumps(response))
