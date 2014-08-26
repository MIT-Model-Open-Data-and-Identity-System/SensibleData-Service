from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from collections import defaultdict
from authorization_manager import authorization_manager
import bson
import bson.json_util as json
import logging
import database
import re

def getLogger(name):
    logger = logging.getLogger('sensible.' + name)
    return logger

log = getLogger(__name__)

def message(request, data={}, user={}):
    req = {}
    req['path'] = request.path

    if hasattr(user, 'username'): req['user'] = user.username

    if 'meta' in data and 'api_call' in data['meta']:

        req_audited = req.copy()
        req_audited['accesses'] = {}

        if data['meta']['api_call'] is not None and isinstance(data['meta']['api_call'], dict):
            req_audited['meta'] = data['meta']['api_call']
            req_audited['count'] = data['meta']['results_count']
        if True or data['results'] is not None and isinstance(data['results'], list) and data['meta']['results_count'] > 0:

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

def processApiCall(request):
  params = {'week' : None, 'year' : None, 'researcher' : None}
  api_params = ['bearer_token', 'week', 'year', 'researcher']
  for k in request.REQUEST.keys():
    if k not in api_params:
      raise BadRequestException('error',400, str(k) + ' is not a legal API parameter.'\
          +' Legal API parameters are: ' + ', '.join(api_params))

  ### deal with start_date and end_date
  if request.REQUEST.get('week',None) is not None:
    try:
      params['week'] = int(request.REQUEST.get('week'))
    except ValueError:
      raise BadRequestException('error',400,request.REQUEST.get('week') + ' is not a valid value for the week parameter. Use an integer value')
  if request.REQUEST.get('year',None) is not None:
    try:
      params['year'] = int(request.REQUEST.get('year'))
    except:
      raise BadRequestException('error',400,request.REQUEST.get('year') + ' is not a valid value for the year parameter. Use an integer value')
  if request.REQUEST.get('researcher',None) is not None:
    params['researcher'] = request.REQUEST.get('researcher')
  return params

def raw_accesses(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  params = processApiCall(request)
  if params['researcher'] is None:
    raise BadRequestException('error',400, 'Researcher id is missing. It is required.')

  db = database.AuditDB()
  docs = db.get_raw_accesses(auth['user'].username, params['researcher'], params['week'], params['year'])
  response = {'name' : 'raw_accesses', 'results' : docs['results'], 'meta' : docs['meta']}
  return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def weekly_accesses(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  params = processApiCall(request)

  db = database.AuditDB()
  docs = db.get_weekly_user_accesses(auth['user'].username, params['year'])
  response = {'name' : 'weekly_accesses', 'results' : docs['results'], 'meta' : docs['meta']}
  return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def accesses(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  params = processApiCall(request)

  db = database.AuditDB()
  docs = db.get_user_accesses(auth['user'].username, params['week'], params['year'])
  response = {'name' : 'user_accesses', 'results' : docs['results'], 'meta' : docs['meta']}
  return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def weekly_researchers(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  params = processApiCall(request)

  db = database.AuditDB()

  docs = db.get_weekly_researcher_accesses(params['year'])
  response = {'name' : 'weekly_researcher_accesses', 'results' : docs['results'], 'meta' : docs['meta']}
  return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def researchers(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  params = processApiCall(request)

  db = database.AuditDB()

  docs = db.get_avg_accesses(params['week'], params['year'])
  response = {'name' : 'researcher_accesses', 'results' : docs['results'], 'meta' : docs['meta']}
  return HttpResponse(json.dumps(response), content_type="application/json", status=200)

def researchers_average(request):

  # authenticate the request
  auth = authorization_manager.authenticate_token(request)

  if 'error' in auth:
    response = {'meta':{'status':{'status':'error','code':401,'desc':auth['error']}}}
    log.error(message(request, response))
    return HttpResponse(json.dumps(response), status=401, content_type="application/json")

  params = processApiCall(request)

  db = database.AuditDB()

  docs = db.get_weekly_avg_accesses(params['year'])
  response = {'name' : 'researcher_requests', 'results' : docs['results'], 'meta' : docs['meta']}
  return HttpResponse(json.dumps(response), content_type="application/json", status=200)

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
