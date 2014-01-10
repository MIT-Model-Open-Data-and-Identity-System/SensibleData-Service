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
import os
from backup import backup
import re
import random
import collections

from models import Voucher
from games import clean_game, get_game

import connectors.connectors_config

from pprint import pformat


connector_conf = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']

# TODO: Dictator game cannot end atm, as only one participant answers. Not a big deal, as we might not use it.


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


    query = {'participant': user.username}

    vouchers = Voucher.objects.filter(won_by = user)

    return HttpResponse(json.dumps({
        'current':games,
        'codes': [{"code":v.voucher, "timestamp":int(time.mktime(v.won_at.utctimetuple()))} for v in vouchers]
    }))


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
        game['answers'] = []

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

    import tasks
    log = tasks.populate_answers()

    r = ""
    for l in log:
        r += str(l)+"<br/>\n\n"

    return HttpResponse(r)



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

    if not request.REQUEST.get('game_id') or not request.REQUEST.get('answer') or not request.REQUEST.get('opened'):
        return HttpResponse(json.dumps({'status': 'error', 'error': 'Must define game_id, answer and opened'}), status=200)

    answer = {}
    answer['answer'] = urllib.unquote(request.REQUEST.get('answer'))
    answer['game_id'] = urllib.unquote(request.REQUEST.get('game_id'))
    answer['opened'] = urllib.unquote(request.REQUEST.get('opened'))
    answer['answered'] = time.time()
    answer['user'] = user.username

    if roles: answer['user_roles'] = roles

    probe = 'dk_dtu_compute_economics_answers'

    backup.backupValue(data=answer, probe=probe, user=user.username)

    answers_path = connector_conf['answers_path']

    if not os.path.exists(answers_path):
        os.makedirs(answers_path)

    filename = answer['game_id']+"_"+user.username+'.json'
    filepath = os.path.join(answers_path, filename)

    while os.path.exists(filepath):
        parts = filename.split('.json');
        counted_parts = re.split('__',parts[0]);
        appendix = str(int(random.random()*10000))
        filename = counted_parts[0] + '__' + appendix + '.json'
        filepath = os.path.join(answers_path, filename)

    with open(filepath, "w") as f:
        f.write(json.dumps(answer))

    return HttpResponse(json.dumps({'status': 'ok'}), status=200)




def sendFinishedNotification(participant, code, timestamp):
    return sendNotification(participant, {'title': 'You\'ve won a voucher', 'body':'Press to see it', 'type':'economics-game-finished', 'code': code, 'timestamp': int(timestamp)})

def sendGameStartedNotification(participant, game):
    data = {'title': 'You\'ve been invited to a game', 'body':'You have a chance at winning movie vouchers. Press to see more.', 'type':'economics-game-init'}

    if isinstance(game['participants'], collections.Sequence):
         game['participants'] = len(game['participants'])

    game['started'] = int(game['started'])

    for key,value in game.iteritems():
        data['game-'+key] = value
    return sendNotification(participant, data)

def sendNotification(participant, data):
    gcm_registrations = GcmRegistration.objects.filter(user__username=participant, application__name='Economics Games')

    for gr in gcm_registrations:
        gcm_server.sendNotification(gr.gcm_id, data, '')

    return gcm_registrations
