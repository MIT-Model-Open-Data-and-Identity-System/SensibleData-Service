from celery import task
import connectors.connectors_config
import os
import bson.json_util as json
from utils.database import Database
import time
from bson.objectid import ObjectId

from connector_economics import sendFinishedNotification

connector_conf = connectors.connectors_config.CONNECTORS['ConnectorEconomics']['config']

@task()
def populate_answers(folder=connector_conf['answers_path']):
    database = Database()

    # Disallow secondary reads, as we need to be sure if the game has ended or not
    database.allow_secondary_reads = False

    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".json"):
                file_path = os.path.join(root, f)
                
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
                        return # The game is either ended or doesn't exist.
                    else:
                        game = game[0]

                    if not answer['user'] in game['participants']:
                        os.remove(file_path)
                        return # Not a participant in this game.

                    # This is not defined in insert
                    game['answers'] = game.get('answers',[])

                    if answer['user'] in game['answers']:
                        os.remove(file_path)
                        return # already answered

                    # can use length here as we have made sure that the user is in participants and not in answers
                    if len(game['participants']) == (len(game['answers'])+1):
                        # delete current and insert into finished
                        game['answers'].append(answer['user'])
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
                                        {'$addToSet': {'answers': answer['user']}},
                                        collection='dk_dtu_compute_economics_games_current',
                                        roles=roles)

                    answer['game_type'] = game['type']

                    doc_id = database.insert(answer, collection='dk_dtu_compute_economics_answers', roles=roles)

                os.remove(file_path)

