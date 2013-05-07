from pymongo import MongoClient
import service_config
import SECURE_service_config

class Database:
	client = None
	db = None

	def __init__(self):
		self.client = MongoClient(service_config.DATABASE['params']['url']%(SECURE_service_config.DATABASE['username'],SECURE_service_config.DATABASE['password']))
		self.db = self.client[service_config.DATABASE['params']['database']]

	def insert(self, documents, collection):
		coll = self.db[collection]
		doc_id = coll.insert(documents, continue_on_error=True)
		coll = self.db[collection]


	def getDocuments(self, query, collection):
		coll = self.db[collection]
		return coll.find(query)
