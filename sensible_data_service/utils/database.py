from pymongo import MongoClient
from service_config import Config

class Database:
	client = None
	db = None
	config = None

	def __init__(self):
		self.config = Config()
		self.client = MongoClient(self.config.config['database']['params']['url']%(self.config.secure_config['database']['username'],self.config.secure_config['database']['password']))
		self.db = self.client[self.config.config['database']['params']['database']]

	def insertDocument(self, document, collection):
		coll = self.db[collection]
		doc_id = coll.insert(document)
		return doc_id

	def getDocuments(self, query, collection):
		coll = self.db[collection]
		return coll.find(query)
