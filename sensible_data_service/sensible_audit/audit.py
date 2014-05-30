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

        req_audited = req.copy()
        req_audited['accesses'] = {}

        if data['meta']['api_call'] is not None and isinstance(data['meta']['api_call'], dict):
            req_audited['meta'] = data['meta']['api_call']
            req_audited['count'] = data['meta']['results_count']
        if data['results'] is not None and isinstance(data['results'], list) and data['meta']['results_count'] > 0:

            # extend 'path' field to make it more 'querieble'
            connector_regex = re.compile('.*\/connectors\/(\w*)\/v1\/(\w*)\/')
            pattern = connector_regex.match(request.path)

            if pattern is not None:
                connector = {}
                req_audited['connector'] = pattern.group(1)
                req_audited['probe'] = pattern.group(2)

            accesses_per_user = defaultdict(int)
            for result in data['results']:
                accesses_per_user[result['user']] += 1

            accesses = []
            for user, count in accesses_per_user.iteritems():
              accesses.append({'user' : user, 'count' : count})

            req_audited['accesses'] = accesses

            log.info(req_audited)
        req['meta'] = data['meta']
    else:
        req.update(data)
    return req

def accesses(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  db = database.AuditDB()
  docs = db.get_agg_accesses_researcher_for_user(request.user.username)
  return HttpResponse(json.dumps(docs), content_type="application/json", status=200)

def researchers(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  db = database.AuditDB()

  docs = db.get_agg_accesses_researcher()
  return HttpResponse(json.dumps(docs), content_type="application/json", status=200)
