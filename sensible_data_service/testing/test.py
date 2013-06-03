from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from authorization_manager.authorization_manager import *
import bson.json_util as json
from connector_pipes.connector_pipe_funf import connector_pipe_funf

def testing(request):
	response = 'dupa'
	return HttpResponse(json.dumps(response))

