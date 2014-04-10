from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from authorization_manager import authorization_manager
import bson.json_util as json
import database
import logging

def getLogger(name):
    logger = logging.getLogger('sensible.' + name)
    return logger

log = getLogger(__name__)

def message(request, data={}, results=[]):
    req = {}
    
    req['path'] = request.get_full_path()
    req['method'] = request.method
    #req['remote_addr'] = request.META.get('REMOTE_ADDR')
    #req['remote_host'] = request.META.get('REMOTE_HOST')
    #req['user_agent'] = request.META.get('HTTP_USER_AGENT')

    if hasattr(request, 'user'): req['user'] = request.user.username
    
    if 'meta' in data and 'api_call' in data['meta']:

        req_audited = req.copy()
        req_audited['accesses'] = {}

        if data['meta']['api_call'] is not None and isinstance(data['meta']['api_call'], dict): 
            req_audited.update(data['meta']['api_call'])
        if data['results'] is not None and isinstance(data['results'], list):
            for result in data['results']:
                req_audited['accesses'].setdefault(result['user'],[]).append(result['_id'])
            log.info(req_audited)
        req.update(data['meta'])
    else:
        req.update(data)  
    return req

def accesses(request):
    """
        Queries the database and returns aggregated accesses by researcher.
    """

    # authenticate token
    auth = authorization_manager.authenticate_token(request)

    if 'error' in auth: 
        return response_error(request, auth)

    # read accesses from database
    db = database.AuditDB()
    accesses = db.get_accesses_by_researcher(request.user.username)

    # build response
    context = {'accesses': accesses}
    return HttpResponse(json.dumps(accesses))

def response_error(request, auth):
    response = {'meta': {'status': 'error', 'code': 401, 'desc': auth['error']}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type='application/json')


def dashboard(request):
    # authenticate token
    auth = authorization_manager.authenticate_token(request)

    if 'error' in auth:
        response = {'meta': {'status': 'error', 'code': 401, 'desc': auth['error']}}
        log.error(message(request, response))
        return HttpResponse(json.dumps(response), status=401, content_type='application/json')

    # read accesses from the database
    accesses = dataBuild(request, request.user.username)

    # build response
    context = {'accesses': accesses, 'bearer_token': request.REQUEST.get('bearer_token')}
    return render(request, 'sensible_audit/audit.html', context)

def accesses2(request):
    """
     Shows information about who has access the user's data.
    """
    auth = authorization_manager.authenticate_token(request)

    if 'error' in auth:
        response = {'meta': {'status':
                            {'status': 'error', 'code': 401,
                             'desc': auth['error']}}}
        return HttpResponse(json.dumps(response),
                            status=401, content_type="application/json")

    accesses = dataBuild(request, request.user.username)
    return HttpResponse(json.dumps(accesses), status=200, content_type="application/json")
    

def dataBuild(request, user):
    db = database.AuditDB()
    accesses = db.get_accesses(user)
    return accesses

class BadRequestException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __init__(self, status, code, description):
        self.value = {}
        self.value['status'] = status
        self.value['code'] = code
        self.value['desc'] = description
    
    def __str__(self):
        return repr(self.value)