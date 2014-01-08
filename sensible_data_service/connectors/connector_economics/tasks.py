from celery import task
import connectors.connectors_config
import os
import bson.json_util as json
from utils.database import Database
import time
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from games import get_outcome
from models import Voucher
from django.contrib.auth.models import User

from connector_economics import sendFinishedNotification

connector_conf = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']

@task()
def populate_answers(folder=connector_conf['answers_path']):
    database = Database()

    log=[]

    # Disallow secondary reads, as we need to be sure if the game has ended or not
    database.allow_secondary_reads = False

    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".json"):
                file_path = os.path.join(root, f)
                log.append("\n\nOpening "+file_path)
                
                with open(file_path, "r") as f:
                    answer = json.loads(f.read())

                if 'game_id' in answer and 'user' in answer and 'answer' in answer and 'opened' in answer:
                    if 'user_roles' in answer:
                        roles = answer['user_roles']
                        del answer['user_roles']
                    else:
                        roles = None

                    game = database.getDocuments({'_id': ObjectId(answer['game_id'])},
                                                collection='dk_dtu_compute_economics_games_current',
                                                roles=roles)
                    
                    if game.count()==0:
                        os.remove(file_path)
                        log.append("Game doesn't exist")
                        continue # The game is either ended or doesn't exist.
                    else:
                        game = game[0]
                    
                    log.append("Game "+repr(game))
                    
                    if not answer['user'] in game['participants']:
                        os.remove(file_path)
                        log.append("User not in participants")
                        continue # Not a participant in this game.

                    # This is not defined in insert
                    game['answers'] = game.get('answers',[])

                    if answer['user'] in [ua['user'] for ua in game['answers']]:
                        log.append("Already answered")
                        os.remove(file_path)
                        continue # already answered

                    log.append(str(len(game['participants']))+"=="+str(len(game['answers'])+1))

                    user_answer = {'user':answer['user'], 'answer':answer['answer']}
                    
                    # can use length here as we have made sure that the user is in participants and not in answers
                    if len(game['participants']) == (len(game['answers'])+1):
                        # delete current and insert into finished
                        game['answers'].append(user_answer)
                        try:
                            database.remove(game['_id'], collection='dk_dtu_compute_economics_games_current', roles=roles)
                            database.insert(game, collection='dk_dtu_compute_economics_games_finished', roles=roles)

                            # Code allocation
                            voucher_allocation = get_outcome(game)
                            log.append("voucher_allocation: "+repr(voucher_allocation))
                            num_vouchers = sum(voucher_allocation.values())
                            log.append("num_vouchers: "+repr(num_vouchers))
                            vouchers = Voucher.objects.filter(won_by__isnull = True)[0:num_vouchers]
                            
                            i = 0
                            for user, num_vouchers_for_user in voucher_allocation.iteritems():
                                voucher_ids = [v.id for v in vouchers[i:num_vouchers_for_user]]
                                log.append("giving "+repr(voucher_ids)+" to "+user)
                                
                                Voucher.objects.filter(id__in = voucher_ids).update(won_by = User.objects.get(username=user))

                                i+=num_vouchers_for_user

                            # Send notifications
                            for participant in game['participants']:
                                sendFinishedNotification(participant,"code"+str(time.time()), time.time())
                        except DuplicateKeyError, e:
                            log.append("DuplicateKeyError")
                    else:
                        database.update({'_id': game['_id']},
                                        {'$addToSet': {'answers': user_answer}},
                                        collection='dk_dtu_compute_economics_games_current',
                                        roles=roles)

                    answer['game_type'] = game['type']

                    doc_id = database.insert(answer, collection='dk_dtu_compute_economics_answers', roles=roles)

                os.remove(file_path)

    return log