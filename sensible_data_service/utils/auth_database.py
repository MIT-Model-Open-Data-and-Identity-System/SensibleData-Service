from pymongo import MongoClient
import service_config
import SECURE_service_config

#TODO: delete this module?

class AuthDatabase(object):
        client = None
        db = None

        def __init__(self):
                self.client = MongoClient(service_config.AUTH_DATABASE['params']['url']%(SECURE_service_config.AUTH_DATABASE['username'],SECURE_service_config.AUTH_DATABASE['password']))
                self.db = self.client[service_config.AUTH_DATABASE['params']['database']]

        def insert(self, document, collection):
                coll = self.db[collection]
                doc_id = coll.insert(document)
                return doc_id

        def getDocuments(self, query, collection):
                coll = self.db[collection]
                return coll.find(query)
