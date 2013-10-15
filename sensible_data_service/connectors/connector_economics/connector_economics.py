from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from authorization_manager import authorization_manager
from accounts.models import UserRole
from connectors.connector import connector
import bson.json_util as json

#from connectors.connector_funf.models import ConnectorFunf
import connectors.connectors_config;


# bug fix
# see http://stackoverflow.com/questions/13193278/understand-python-threading-bug
# import threading
# threading._DummyThread._Thread__stop = lambda x: 42
# end of bug fix



myConnector = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']


@csrf_exempt
def answer(request):
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    roles = None
    try:
        roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
    except:
        pass

	return HttpResponse(status='200')



@csrf_exempt
def list(request):
    #TODO: different scope?
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    return HttpResponse(json.dumps({'current':[{'type':'pgg', 'participants':4}, {'type':'pgg', 'participants':1337}]}))
