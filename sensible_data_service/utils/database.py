from pymongo import MongoClient
import service_config
import SECURE_service_config

class Database:
	client = None
	db = None

	def __init__(self):
		self.client = MongoClient(service_config.DATABASE['params']['url']%(SECURE_service_config.DATABASE['username'],SECURE_service_config.DATABASE['password']))
		self.db = self.client[service_config.DATABASE['params']['database']]

	def insert(self, document, collection):
		coll = self.db[collection]
		doc_id = coll.insert(document)
		return doc_id

	def getDocuments(self, query, collection):
		coll = self.db[collection]
		return coll.find(query)
