from django.http import HttpResponse
import json
from utils import NON_SECURE_CONFIG
import pymongo
from utils.trail import Trail
from utils.keystore import Keystore
from utils import helper

# TODO: key derivation from password and other params
# TODO: key substitution/renovation in case it has been broken or lost
# TODO: chain restore if chain breaks
# TODO: automatic/routine/cronjob verification between checksum and what saved in the big DB. If problems, inform the user and ask for providing the key for chain verification. 


class Auditor(object):

    data_client = None
    data_db = None

    trail = None
    keystore = None


    def __init__(self):
        # Setup connection for fetching the fake data:
        self.data_client = pymongo.MongoClient(NON_SECURE_CONFIG.DATA_DATABASE['params']['url']%(NON_SECURE_CONFIG.DATA_DATABASE['params']['username'],NON_SECURE_CONFIG.DATA_DATABASE['params']['password']))
        self.data_db = self.data_client[NON_SECURE_CONFIG.DATA_DATABASE['params']['database']]
        self.trail = Trail()
        self.keystore = Keystore()



# API methods:
    def append(self, study, user, data):

#data extraction/treatment from the entry
        collection_id = study + "_" + user

# entry field creation
        timestamp = helper.get_timestamp() 
        flow_id = self.trail.get_max_flow_id(collection_id) + 1
        saved_data = helper.extract_info(data)
        checksum = helper.checksum(saved_data)
        study_user_key = self.keystore.get_key(collection_id)
        previous_link = self.trail.get_link(collection_id, flow_id -1 )
        link = helper.link(checksum, previous_link, str(study_user_key))
        self.update_key(collection_id)     
        entry = self.assemble(collection_id, flow_id, saved_data, checksum, link)
        entry_id = self.trail.append(collection_id, entry) # finally, append
        returned = (collection_id, flow_id, entry_id)
        return returned

    def verify(self, study, user, start, stop):
        pass


#######################################################################################

# Internal methods, not provided as APIs:
    def get_study_user_trail(self, study, user):
        collection_id = study + "_" + user
        returned = self.trail.get_study_user_trail(collection_id)
        return returned

    def get_previous_entry(self, study, username, flow_id):
        collection_id = study + "_" + user
        returned = self.trail.get_study_user_entry(collection_id, flow_id-1)
        return returned
    
    def update_key(self, collection_id):
        key = self.keystore.get_key(collection_id)
        key = helper.do_hash(1,key)
        self.keystore.update_key(collection_id, key)
       
# TODO: to change with key derivation function   
# TODO: add control: set a key only if for that collection the key does NOT exist yet. If it does, throw an exeption [ask for updating maybe, instead]       

    def assemble(self, collection_id, flow_id, saved_data, checksum, link):
        entry = {"flow_id":flow_id, "saved_data":saved_data, "checksum":checksum, "link":link}
        return entry

    def user_enrollment(self, collection_id, key):
        key = self.set_key(collection_id, key)
        collection = self.start_collection(collection_id)
        return (key, collection)

    def start_collection(self, collection_id):
        return self.assemble(collection_id, NON_SECURE_CONFIG.SETUP["flow_id"], NON_SECURE_CONFIG.SETUP["saved_data"], NON_SECURE_CONFIG.SETUP["checksum"], NON_SECURE_CONFIG.SETUP["link"])
    
    def set_key(self, collection_id, key):
        return self.keystore.set_key(collection_id, key)

