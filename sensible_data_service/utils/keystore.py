import pymongo
import NON_SECURE_CONFIG

class Keystore(object):

    keytable = None

    def __init__(self):
        client = pymongo.MongoClient(NON_SECURE_CONFIG.TRAIL_DATABASE['params']['url']%(NON_SECURE_CONFIG.TRAIL_DATABASE['params']['username'],NON_SECURE_CONFIG.TRAIL_DATABASE['params']['password']))
        db = client[NON_SECURE_CONFIG.TRAIL_DATABASE['params']['database']]
        self.keytable = db[NON_SECURE_CONFIG.TRAIL_DATABASE['params']['keystore']]

# TODO: change find_one with find_all and check that it MUST return ONLY 1 value. In other case, raise an exeption
    def get_key(self, collection_id):
        return self.keytable.find_one({"study_username" : collection_id}).get("key")

    def update_key(self, collection_id, key):
        return self.keytable.update({ "study_username": collection_id }, { "$set": { "key": key } } )

    def set_key(self, collection_id, key):
        return self.keytable.insert({ "study_username" : collection_id, "key" : key})
