# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from authorization_manager import authorization_manager
from accounts.models import UserRole
from connectors.connector import connector
import bson.json_util as json
import urllib
from utils.database import Database
import time
import uuid

import connectors.connectors_config;


# bug fix
# see http://stackoverflow.com/questions/13193278/understand-python-threading-bug
# import threading
# threading._DummyThread._Thread__stop = lambda x: 42
# end of bug fix



myConnector = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']


#TODO: Find type
#TODO: Update the game to figure out when the game is finished
#TODO: Get codes from somewhere (make sure not to select the same twice)
#TODO: Send gcm notifications when games are finished (to winners)
@csrf_exempt
def answer(request):
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    roles = None
    try:    roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
    except: pass

    database = Database()

    game = json.loads(
            database.getDocuments({'_id': urllib.unquote(request.REQUEST.get('_id'))},
                                collection='dk_dtu_compute_economics_games', roles=roles))

    if not user.username in game.participants:
        return HttpResponse(json.dumps({'error': 'You are not a participant in this game.'}), status=401)

    answer = {}
    answer['answer'] = urllib.unquote(request.REQUEST.get('answer'))
    answer['type'] = game['type']
    answer['game_id'] = game['_id']
    answer['_id'] = game['_id']+user.username # Add username so that there can be multiple answers to one game.
    answer['user'] = user.username

    doc_id = database.insert(answer, collection='dk_dtu_compute_economics_answers', roles=roles)

    return HttpResponse(status=200)


#TODO: Get codes from a real codes collection
@csrf_exempt
def list(request):
    #TODO: different scope?
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    roles = None
    try:    roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
    except: pass

    database = Database()

    query = {'participants': {'$all': [user.username]}}

    games = database.getDocuments(query, collection='dk_dtu_compute_economics_games', roles=roles)

    # Clean up
    games = [{'_id': game['_id'],
              'type': game['type'],
              'participants': len(game['participants']),
              'started': game['started']} for game in games]

    return HttpResponse(json.dumps({
        'current':games,
        'codes':[
            {'code': 'hmngifoækhfgoøh', 'timestamp': 1382558020},
            {'code': '68u59000jh', 'timestamp': (int)(time.time())}
        ]}))

    return HttpResponse(json.dumps({
        'current':[
            {'_id': '19157053-70f2-4ef0-968c-da6bf44a24d2', 'type':'game-pgg', 'participants':3, 'started':(int)(time.time()-60)},
            {'_id': 'ff43036b-1df0-4228-a76c-e8bfca3cb878', 'type':'game-dg-proposer', 'participants':2, 'started':(int)(time.time()-6000)},
            {'_id': 'ae566676-eb5b-494c-a843-8e41f8ad84fd', 'type':'game-dg-responder', 'participants':2, 'started':1382558020}
        ],
        'codes':[
            {'code': 'hmngifoækhfgoøh', 'timestamp': 1382558020},
            {'code': '68u59000jh', 'timestamp': (int)(time.time())}
        ]}))


#TODO: Make an interface to this
#TODO: Select users at random?
#TODO: get researcher or developer acc to test with
#TODO: send gcm notifications
@csrf_exempt
def create_game(request):
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    roles = None
    try:    roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
    except: pass



    # if roles and ('researcher' in roles or 'developer' in roles):
    if True:
        database = Database()
        game = {'_id': str(uuid.uuid4()), 'started': int(time.time())}
        game['type'] = urllib.unquote(request.REQUEST.get('type'))
        game['participants'] = [user.username]

        participant_roles = request.REQUEST.getlist('roles')

        doc_id = database.insert(game, collection='dk_dtu_compute_economics_games', roles=participant_roles)

        return HttpResponse(json.dumps(game))

    return HttpResponse(json.dumps({'error': 'You do not have sufficient permissions to add a game.'}), status=401)
