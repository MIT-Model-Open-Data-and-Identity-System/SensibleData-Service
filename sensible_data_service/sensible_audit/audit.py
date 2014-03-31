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