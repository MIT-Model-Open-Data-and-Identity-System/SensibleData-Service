from django.http import HttpResponse
import json
from utils import NON_SECURE_CONFIG
import pymongo
from utils.trail import Trail
from utils.keystore import Keystore
from utils import helper
from Crypto.Hash import SHA256

# Verification
# TODO: key derivation from password and other params
# TODO: automatic/routine/cronjob verification between checksum and what saved in the big DB. If problems, inform the user and ask for providing the key for chain verification. 
# TOMO: key substitution/renovation in case it has been broken or lost
# TOMO: chain restore if chain breaks
# TOMO: Permissions


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


#######################################################################################
# API methods:
#######################################################################################
    def append(self, collection_id, data):

#data extraction/treatment from the entry

# entry field creation
        timestamp = helper.get_timestamp() 
        flow_id = self.trail.get_max_flow_id(collection_id) + 1
        saved_data = helper.extract_info(data)
        checksum = helper.checksum(saved_data)
        study_user_key = self.keystore.get_key(collection_id)
        previous_link = self.trail.get_link(collection_id, flow_id -1 )
        link = helper.link(checksum, previous_link, str(study_user_key))
        self.update_key(collection_id)     
        entry = self.assemble(timestamp, flow_id, saved_data, checksum, link) # <timestamp, flow_id, saved_data, checksum, link>
        entry_id = self.trail.append(collection_id, entry) # finally, append
        returned = (collection_id, flow_id, entry_id)
        return returned

# Whatch out on timing-attacks. Read more about "break-on-inequality" algorithm to compare a candidate HMAC digest with the calculated digest is wrong.
# Add a caching system. Instead of connecting to the db for every single entry, cache a bunch of them locally.
    def verify(self, collection_id, start, stop):

        keep_looking = True
        audit = {}
        index = start

        while (keep_looking and index <= stop):
# get a single entry:
            current_entry = self.trail.get_study_user_entry(collection_id, start)
            print current_entry

# check saved_data against checksum in the same entry: current saved data and current checksum. No key involved.
# check chain link: this checksum, the previous link and the previous key [to be generated from the master secret key] is equal to the current store value?

            index = index + 1

        return audit


#    def user_enrollment(self, collection_id, key):
#        key = self.set_key(collection_id, key)
#        collection = self.start_collection(collection_id)
#        return (key, collection)


# TODO: add check if the 3-ple is not already present.
    def user_enrollment(self, username, client_id):

        collection_id = username + "_" + str(client_id)
# Check if already present:
        if (self.get_study_user_trail(collection_id)):
            print "Already present"
            return False

# get secrets using clien_id and platform config file

        client_secret = "fake_secret"
        platform_secret = "fake_secret"

        h = SHA256.new()
        h.update(username + client_secret + platform_secret)
        key = h.hexdigest()

        key_id = self.set_key(collection_id, key)
        entry_id = self.start_collection(collection_id)
        return (key)

#######################################################################################
# Internal methods:
#######################################################################################
    def get_study_user_trail(self, collection_id):
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
       

# TODO: add control: set a key only if for that collection the key does NOT exist yet. If it does, throw an exeption [ask for updating maybe, instead]      
# TODO: move this to the trail, since it is DB dependent
    def assemble(self, timestamp, flow_id, saved_data, checksum, link):
        entry = {"timestamp":timestamp, "flow_id":flow_id, "saved_data":saved_data, "checksum":checksum, "link":link}
        return entry


    def start_collection(self, collection_id):
        timestamp = helper.get_timestamp() 
        entry = self.assemble(timestamp, NON_SECURE_CONFIG.SETUP["flow_id"], NON_SECURE_CONFIG.SETUP["saved_data"], NON_SECURE_CONFIG.SETUP["checksum"], NON_SECURE_CONFIG.SETUP["link"])
        returned = self.trail.insert(collection_id, entry)
        return returned

    def set_key(self, collection_id, key):
        return self.keystore.set_key(collection_id, key)

