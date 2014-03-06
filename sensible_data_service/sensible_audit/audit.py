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

def message(request, data={}, results=[]):
    req = {}
    
    req['path'] = request.get_full_path()
    req['method'] = request.method
    req['remote_addr'] = request.META.get('REMOTE_ADDR')
    #req['remote_host'] = request.META.get('REMOTE_HOST')
    req['user_agent'] = request.META.get('HTTP_USER_AGENT')

    if hasattr(request, 'user'): req['user'] = request.user.username
    
    if 'meta' in data and 'api_call' in data['meta']:
        if data['meta']['api_call'] is not None and isinstance(data['meta']['api_call'], dict): req.update(data['meta']['api_call'])
        if data['results'] is not None and isinstance(data['results'], list):
            queries = [result['_id'] for result in data['results']]
            req.update({'results': queries})    
    return req

def visualization(request):
    """
     Shows information about who has access the user's data.
    """
    auth = authorization_manager.authenticate_token(request)

    if 'error' in auth:
        response = {'meta': {'status':
                            {'status': 'error', 'code': 401,
                             'desc': auth['error']}}}
        log.error('authentication error', extra=build_request_dict(request))
        return HttpResponse(json.dumps(response),
                            status=401, content_type="application/json")

    log.info('audit data accessed', extra=build_request_dict(request))
    accesses = dataBuild(request, request.user.username)
    return HttpResponse(json.dumps(accesses), status=200, content_type="application/json")
    

def accesses(request):
    return get_data(request)

def get_data(request):
    auth = authorization_manager.authenticate_token(request)

    if 'error' in auth:
        response = {'meta': {'status':
                            {'status': 'error', 'code': 401,
                             'desc': auth['error']}}}
        log.error('authentication error', extra=build_request_dict(request))
        return HttpResponse(json.dumps(response),
                            status=401, content_type="application/json")

    log.info('audit data accessed', extra=build_request_dict(request))
    accesses = dataBuild(request, request.user.username)
    return render(request, 'sensible_audit/audit.html', {'accesses': accesses, 'token': request.REQUEST.get('bearer_token')})

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