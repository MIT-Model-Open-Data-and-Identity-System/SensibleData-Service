from django.http import HttpResponse
import json
from utils import NON_SECURE_CONFIG
import pymongo
from utils.trail import Trail
from utils.keystore import Keystore
from utils import helper
from Crypto.Hash import SHA256
import hashlib

# TODO: key derivation from password and other params
# TODO: automatic/routine/cronjob verification between checksum and what saved in the big DB. If problems, inform the user and ask for providing the key for chain verification. 
# TOMO: key substitution/renovation in case it has been broken or lost
# TOMO: chain restore if chain breaks
# TOMO: Permissions

	
class Auditor(object):
		
    trail = None
    evolving_keystore = None
    secret_keystore = None
		
    def __init__(self):
        # Setup connection for fetching the fake data:
        self.trail = Trail()
        self.evolving_keystore = Keystore("evolving")
        self.secret_keystore = Keystore("secret")
        print "HERE"

#######################################################################################
# API methods:
######################################################################################
    def user_enrollment(self, client_id, username):
        status = {}
        collection_id = helper.collection_format(client_id, username)
	
        if (self.get_study_user_trail(collection_id) or self.evolving_keystore.exists_collection(collection_id)):
            status["code"] = -1
            status["data"] = "3-ple username, client_secret, platform_secret already present in the trail"
            return status

        key = self.create_key(collection_id, username, client_id)
        entry_id = self.start_collection(collection_id)

        status["code"] = 0
        status["data"] = key
        return status



    def append(self, collection_id, data):
# sanity checks on: 
# collection_id [not None, not null, be sure that already exists]
# data: that is of the agreed format

# entry field creation
        timestamp = helper.get_timestamp() 
        flow_id = self.trail.get_max_flow_id(collection_id) + 1
        saved_data = helper.extract_info(data)
        checksum = helper.checksum(saved_data)
        study_user_key = self.evolving_keystore.get_key(collection_id)
        previous_link = self.trail.get_link(collection_id, flow_id -1 )
        link = helper.link(checksum, previous_link, str(study_user_key))
        self.update_key(collection_id)     
        entry = self.assemble(timestamp, flow_id, saved_data, checksum, link) # <timestamp, flow_id, saved_data, checksum, link>
        entry_id = self.trail.insert(collection_id, entry) # finally, append
        returned = (collection_id, flow_id)
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



#######################################################################################
# Internal methods:
#######################################################################################
    def get_study_user_trail(self, collection_id):
        returned = self.trail.get_study_user_trail(collection_id)
        return returned


    def get_previous_entry(self, study, username, flow_id):
        collection_id = helper.collection_format(study, username)
        returned = self.trail.get_study_user_entry(collection_id, flow_id-1)
        return returned


       
### Log related ###
# TODO: move this to the trail, since it is DB dependent
    def assemble(self, timestamp, flow_id, saved_data, checksum, link):
        entry = {"timestamp":timestamp, "flow_id":flow_id, "saved_data":saved_data, "checksum":checksum, "link":link}
        return entry


    def start_collection(self, collection_id):
        timestamp = helper.get_timestamp() 
        entry = self.assemble(timestamp, NON_SECURE_CONFIG.SETUP["flow_id"], NON_SECURE_CONFIG.SETUP["saved_data"], NON_SECURE_CONFIG.SETUP["checksum"], NON_SECURE_CONFIG.SETUP["link"])
        returned = self.trail.insert(collection_id, entry)
        return returned


### Key related ##

# TODO: get secrets using client_id and platform config file
    def create_key(self, collection_id, username, client_id):
        client_secret = self.get_client_secret(client_id)
        platform_secret = self.get_platform_secret()
        key = None
        if ( not self.evolving_keystore.exists_collection(collection_id) ):
            key = hashlib.sha256(str(username)+str(client_secret)+str(platform_secret)).hexdigest()
            self.evolving_keystore.set_key(collection_id, key)
        return key

    def get_client_secret(self, client_id):
#TODO:  Do something to fetch the secret using the client_id
        return "fake_client_secret"

    def get_platform_secret(self):
# TODO: Do something
        return "fake_platform_secret"


    def update_key(self, collection_id):
        key = None
        print self.evolving_keystore.exists_collection(collection_id)
        if ( self.evolving_keystore.exists_collection(collection_id) ):
            key = self.evolving_keystore.get_key(collection_id)
            key = helper.do_hash(1,key)
            self.evolving_keystore.update_key(collection_id, key)
        return key


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

