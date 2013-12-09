# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from authorization_manager import authorization_manager
from application_manager.models import Application, GcmRegistration
from application_manager import gcm_server
from accounts.models import UserRole
from django.contrib.auth.models import User
from connectors.connector import connector
import bson.json_util as json
import urllib
from utils.database import Database
from pymongo.errors import DuplicateKeyError
import time
import uuid
from bson.objectid import ObjectId

from games import clean_game, get_game

import connectors.connectors_config


# bug fix
# see http://stackoverflow.com/questions/13193278/understand-python-threading-bug
# import threading
# threading._DummyThread._Thread__stop = lambda x: 42
# end of bug fix



myConnector = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']


#TODO: Find type (get_game) check allowed answers
#TODO: Get codes from somewhere (make sure not to select the same twice)
@csrf_exempt
def answer(request):
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    try:    roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
    except: roles = None

    database = Database()
    # Disallow secondary reads, as we need to be sure if the game has ended or not
    database.allow_secondary_reads = False

    game = database.getDocuments({'_id': ObjectId(urllib.unquote(request.REQUEST.get('game_id')))},
                                collection='dk_dtu_compute_economics_games_current',
                                roles=roles)
    
    if game.count()==0:
        return HttpResponse(json.dumps({'error': 'The game is either ended or doesn\'t exist.'}), status=404)
    else:
        game = game[0]

    if not user.username in game['participants']:
        return HttpResponse(json.dumps({'error': 'You are not a participant in this game.'}), status=401)

    # This is not defined in insert
    game['answers'] = game.get('answers',[])

    if user.username in game['answers']:
        return HttpResponse(json.dumps({'status': 'already_answered'}))

    # can use length here as we have made sure that the user is in participants and not in answers
    if len(game['participants']) == (len(game['answers'])+1):
        # delete current and insert into finished
        game['answers'].append(user.username)
        try:
            database.remove(game['_id'], collection='dk_dtu_compute_economics_games_current', roles=roles)
            database.insert(game, collection='dk_dtu_compute_economics_games_finished', roles=roles)
            # Send notifications
            for participant in game['participants']:
                sendFinishedNotification(participant,"code"+str(time.time()), time.time())
        except DuplicateKeyError, e:
            pass
    else:
        database.update({'_id': game['_id']},
                        {'$addToSet': {'answers': user.username}},
                        collection='dk_dtu_compute_economics_games_current',
                        roles=roles)

    answer = {}
    answer['answer'] = urllib.unquote(request.REQUEST.get('answer'))
    answer['type'] = game['type']
    answer['game_id'] = game['_id']
    answer['opened'] = urllib.unquote(request.REQUEST.get('opened'))
    answer['answered'] = time.time()
    answer['user'] = user.username

    doc_id = database.insert(answer, collection='dk_dtu_compute_economics_answers', roles=roles)
    

    return HttpResponse(json.dumps(game), status=200)


#TODO: Get codes from a real codes collection
@csrf_exempt
def getlist(request):
    #TODO: different scope?
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)

    user = auth['user']

    try:    roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
    except: roles = None

    database = Database()

    query = {'participants': {'$all': [user.username]}}

    games = database.getDocuments(query, collection='dk_dtu_compute_economics_games_current', roles=roles)

    # Clean up
    games = [clean_game(game) for game in games]

    return HttpResponse(json.dumps({
        'current':games,
        'codes':[
            {'code': '167416156', 'timestamp': 1382558020},
            {'code': '491657168', 'timestamp': (int)(time.time())}
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
        game = {'started': int(time.time())}
        game['type'] = urllib.unquote(request.REQUEST.get('type'))
        game['participants'] = [user.username]

        for participant in game['participants']:
            sendGameStartedNotification(participant, clean_game(game))

        doc_id = database.insert(game, collection='dk_dtu_compute_economics_games_current', roles=None)

	    #TODO: put id into game.
        return HttpResponse(json.dumps(game))

    return HttpResponse(json.dumps({'error': 'You do not have sufficient permissions to add a game.'}), status=401)


def test(request):
    auth = authorization_manager.authenticate_token(request, 'connector_economics.submit_data')
    if 'error' in auth:
        return HttpResponse(json.dumps(auth), status=401)
    
    user = auth['user']
    participant = user.username
    
    participant = user.username

    dump = []

    for reg in sendFinishedNotification(participant, 'code', time.time()):
        dump.append(reg.gcm_id)

    for reg in sendGameStartedNotification(participant, {'_id': "funkyid",
              'type': 'game-pdg',
              'participants': [1, 2],
              'started': time.time()}):
        dump.append(reg.gcm_id)
    
    return HttpResponse(json.dumps(dump))


def sendFinishedNotification(participant, code, timestamp):
    return sendNotification(participant, {'title': 'You\'ve won a voucher', 'body':'Press to see it', 'type':'economics-game-finished', 'code': code, 'timestamp': timestamp})

def sendGameStartedNotification(participant, game):
    data = {'title': 'You\'ve been invited to a game', 'body':'You have a chance at winning movie vouchers. Press to see more.', 'type':'economics-game-init'}
    for key,value in game.iteritems():
        data['game-'+key] = value
    return sendNotification(participant, data)

def sendNotification(participant, data):
    gcm_registrations = GcmRegistration.objects.filter(user__username=participant, application__name='Economics Games')

    for gr in gcm_registrations:
        gcm_server.sendNotification(gr.gcm_id, data, '')

    return gcm_registrations
