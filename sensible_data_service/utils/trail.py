import pymongo
import NON_SECURE_CONFIG

import json
from django.http import HttpResponse

### Move it to utils
### Change the CONFIG file

class Trail(object):

    client = None
    trail = None

    def __init__(self):
    
        # Setup the connection to the db hosting the log
        self.client = pymongo.MongoClient(NON_SECURE_CONFIG.TRAIL_DATABASE['params']['url']%(NON_SECURE_CONFIG.TRAIL_DATABASE['params']['username'],NON_SECURE_CONFIG.TRAIL_DATABASE['params']['password']))
        self.trail = self.client[NON_SECURE_CONFIG.TRAIL_DATABASE['params']['database']]


# One collection every pair of <study, user>. collection_id = "<study_id> underscore <user_id>" = sensibledtu_riccardo
    def append(self, collection_id, entry):
        collection = self.trail[collection_id]
        record_id = collection.insert(entry)
        return str(record_id)

    def get_study_user_trail(self, collection_id):
        collection = self.trail[collection_id].find()
        return list(collection)   

    def get_max_flow_id(self, collection_id):
        max_flow_id = 0
        resultEntry = self.trail[collection_id].find_one(sort=[("flow_id", -1)])
        if (resultEntry is not None):
            max_flow_id = resultEntry['flow_id']
        return max_flow_id

    def get_study_user_entry(self, collection_id, flow_id):
        print "flow id = ", flow_id, " collection_id = ", collection_id

        result = self.trail[collection_id].find_one({"flow_id" : flow_id})
        print result
        return result

    def get_link(self, collection_id, flow_id):
        previous = self.get_study_user_entry(collection_id, flow_id) 
        return previous.get("link")
