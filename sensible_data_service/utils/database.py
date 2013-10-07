from pymongo import MongoClient, MongoReplicaSetClient
import SECURE_settings
from django.conf import settings
import pymongo

class Database:
	client = None
	db = None
	is_replica_set = False
	replica_set = ""
	ssl = False
	allow_secondary_reads = False
	nodes = []
	database = ""

	def __init__(self):
		try: self.is_replica_set = settings.DATA_DATABASE['is_replica_set']
		except KeyError: pass
		
		try: self.replica_set = settings.DATA_DATABASE['replica_set']
		except KeyError: pass
		
		try: self.ssl = settings.DATA_DATABASE['ssl']
		except KeyError: pass
		
		try: self.allow_secondary_reads = settings.DATA_DATABASE['allow_secondary_reads']
		except KeyError: pass

		self.nodes = settings.DATA_DATABASE['nodes']
		self.database = settings.DATA_DATABASE['database']

		if self.is_replica_set:
			self.client = MongoReplicaSetClient('mongodb://%s/%s'%(','.join(self.nodes), self.database), ssl=self.ssl, replicaSet=self.replica_set)
			self.db = self.client[settings.DATA_DATABASE['database']]
		else:
			self.client = MongoClient('mongodb://%s/%s'%(','.join(self.nodes), self.database), ssl=self.ssl)
			self.db = self.client[settings.DATA_DATABASE['database']]
	
		self.db.authenticate(SECURE_settings.DATA_DATABASE['username'],SECURE_settings.DATA_DATABASE['password'])


	def insert(self, documents, collection, roles = None):
		if roles and 'developer' in roles:
			collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'
		coll = self.db[collection]
		doc_id = coll.insert(documents, continue_on_error=True)
		return doc_id

	def getDocuments(self, query, collection, roles = None, from_secondary = True):
		if roles and 'developer' in roles:
			collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'

		if from_secondary and self.allow_secondary_reads:
			self.db.read_preference = pymongo.ReadPreference.SECONDARY_PREFERRED

		coll = self.db[collection]
		return coll.find(query)

	def getDocumentsCustom(self, query, collection, fields, roles = None, from_secondary = True):
		if roles and 'developer' in roles:
			collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'
		
		if from_secondary and self.allow_secondary_reads:
			self.db.read_preference = pymongo.ReadPreference.SECONDARY_PREFERRED
		
		coll = self.db[collection]
		return coll.find(query, fields)
