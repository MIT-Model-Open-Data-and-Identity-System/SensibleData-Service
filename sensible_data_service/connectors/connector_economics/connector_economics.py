import os.path
import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from backup import backup
import pdb;
from django.core.servers.basehttp import FileWrapper
import mimetypes
from utils import log
from django.conf import settings

from connectors.connector import connector
import bson.json_util as json

#from connectors.connector_funf.models import ConnectorFunf
import connectors.connectors_config;
import authorization_manager


# bug fix
# see http://stackoverflow.com/questions/13193278/understand-python-threading-bug
# import threading
# threading._DummyThread._Thread__stop = lambda x: 42
# end of bug fix


import random
import re

myConnector = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']

@csrf_exempt
def answer(request):
	#pdb.set_trace();
	#log.log('Debug', 'GET for config')
	access_token = request.REQUEST.get('access_token', '')
	#authorization = self.pipe.getAuthorization(access_token)

	#TODO: do stuff

	if access_token:
		return HttpResponse(status='200')
	else:
		return HttpResponse(status='500')


