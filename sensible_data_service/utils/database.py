from pymongo import MongoClient
import SECURE_settings
from django.conf import settings

class Database:
	client = None
	db = None
        auditor = None

	def __init__(self):
		self.client = MongoClient(settings.DATA_DATABASE['params']['url']%(SECURE_settings.DATA_DATABASE['username'],SECURE_settings.DATA_DATABASE['password']))
		self.db = self.client[settings.DATA_DATABASE['params']['database']]

                self.auditor = Auditor()                

	def insert(self, documents, collection, roles = None):
		if roles and 'researcher' in roles:
			collection += '_researcher'
		coll = self.db[collection]
		doc_id = coll.insert(documents, continue_on_error=True)
                self.auditor.append(coll, documents) # call for appending in the log
		return doc_id

	def getDocuments(self, query, collection):
		coll = self.db[collection]
                self.auditor.append(coll, documents) # call for appending in the log
		return coll.find(query)

	def getDocumentsCustom(self, query, collection, fields):
		coll = self.db[collection]
		return coll.find(spec=query, fields=fields)
