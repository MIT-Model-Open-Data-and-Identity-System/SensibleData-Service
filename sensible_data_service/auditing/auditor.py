from django.http import HttpResponse
import json
from utils import NON_SECURE_CONFIG
import pymongo
from utils.trail import Trail
from utils.keystore import Keystore
from utils import helper
from Crypto.Hash import SHA256

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

# sanity checks on 
# collection_id [not None, not null, be sure that already exists]
# data: that is of the agreed format

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
        entry_id = self.trail.insert(collection_id, entry) # finally, append
        returned = (collection_id, flow_id, entry_id)
        return returned

# Timing-attacks. Read more about "break-on-inequality" algorithm to compare a candidate HMAC digest with the calculated digest is wrong.
# Add a caching system. Instead of connecting to the db for every single entry, cache a bunch of them locally.
    def verify(self, collection_id, start, stop, key):

        keep_looking = True
        audit = {}
        index = start

        if (stop > self.trail.get_max_flow_id(collection_id)):
            stop = self.trail.get_max_flow_id(collection_id)


        while (keep_looking and index <= stop):
            current_entry = self.trail.get_study_user_entry(collection_id, index) # get a single entry

# check saved_data against checksum in the same entry: current saved data and current checksum. No key involved. Can be automatized
            status_checksum = self.check_checksum(current_entry["saved_data"], current_entry["checksum"])
            if ( not status_checksum["status"] ) :
                keep_looking = False

# check chain link: this checksum, the previous link and the previous key [to be generated from the master secret key] is equal to the current store value?
            previous_link = self.trail.get_link(collection_id, index - 1)
            status_link = self.check_link(previous_link, current_entry["checksum"], current_entry["link"], key, index)
            if ( not status_link["status"]) :
                keep_looking  = False

            audit = {index : [status_checksum["status"], status_link["status"]]}
            index = index + 1

        return audit


# TODO: add check if the 3-ple is not already present.
    def user_enrollment(self, username, client_id):

        collection_id = username + "_" + str(client_id)
        message = ""
        if (self.get_study_user_trail(collection_id)):
            message = message + collection_id + " log already present " 

        if (self.keystore.exists_collection(collection_id)):
            message = message + "entry in the keystore already present"

        if message != "" :
            return message

# get secrets using client_id and platform config file
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

    


# Leave this if later the user changes the pw
    def set_key(self, collection_id, key):
        return self.keystore.set_key(collection_id, key)


    def check_checksum(self, saved_data, checksum):
        status = False
        temp_checksum = helper.checksum(saved_data)
        if ( temp_checksum == checksum):
            status = True
        return {"status": status, "temp_checksum" : temp_checksum}
    
    def check_link(self, previous_link, checksum, link, key, index):
        status = False
        previous_key = helper.do_hash(index - 1, key)
        temp_link = helper.link(checksum, previous_link, previous_key)
        if ( temp_link == link):
            status = True
        return {"status": status, "temp_link" : temp_link}
