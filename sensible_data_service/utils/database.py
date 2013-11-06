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
	default_database = ""
    	open_databases = {}
    	available_databases = {}

	def __init__(self):
		try: self.is_replica_set = settings.DATA_DATABASE['is_replica_set']
		except KeyError: pass

		try: self.replica_set = settings.DATA_DATABASE['replica_set']
		except KeyError: pass

		try: self.ssl = settings.DATA_DATABASE['ssl']
		except KeyError: pass

		try: self.allow_secondary_reads = settings.DATA_DATABASE['allow_secondary_reads']
		except KeyError: pass

		try: self.available_databases = settings.DATA_DATABASE['available_databases']
		except KeyError: pass

		self.default_database = settings.DATA_DATABASE['default_database']


		self.nodes = settings.DATA_DATABASE['nodes']
		self.database = settings.DATA_DATABASE['database']


		if self.is_replica_set:
			self.client = MongoReplicaSetClient('mongodb://%s'%(','.join(self.nodes)), ssl=self.ssl, replicaSet=self.replica_set)
		else:
			self.client = MongoClient('mongodb://%s/%s'%(','.join(self.nodes)), ssl=self.ssl)



	def getDatabase(self, collection):
		base_name = collection
		if 'question_' in collection: base_name = collection.split('question_')[1]
		if base_name in self.available_databases:
			if base_name in self.open_databases:
				db = self.open_databases[base_name]
			else:
				db = self.client[self.available_databases[base_name]]
				db.authenticate(SECURE_settings.DATA_DATABASE['username'],SECURE_settings.DATA_DATABASE['password'])
				self.open_databases[base_name] = db
		else:
			if self.default_database in self.open_databases:
				db = self.open_databases[self.default_database]
			else:
				db = self.client[self.default_database]
				db.authenticate(SECURE_settings.DATA_DATABASE['username'],SECURE_settings.DATA_DATABASE['password'])
				self.open_databases[self.default_database] = db
		return db

	def insert(self, documents, collection, roles = None):
		if roles and 'developer' in roles:
			collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'

		db = self.getDatabase(collection)

		coll = db[collection]
		doc_id = coll.insert(documents, continue_on_error=True)
		return doc_id

	def update(self, query, documents, collection, roles = None, multi = False):
		if roles and 'developer' in roles:
 				collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'
		coll = self.db[collection]
		effect = coll.update(query, documents, multi=multi)
		return effect

	def remove(self, query, collection, roles = None):
		if roles and 'developer' in roles:
 				collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'
		coll = self.db[collection]
		effect = coll.remove(query)
		return effect

	def getDocuments(self, query, collection, roles = None, from_secondary = True):
		if roles and 'developer' in roles:
			collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'

		db = self.getDatabase(collection)

		if from_secondary and self.allow_secondary_reads:
			db.read_preference = pymongo.ReadPreference.SECONDARY_PREFERRED

		coll = db[collection]
		return coll.find(query)

	def getDocumentsCustom(self, query, collection, fields, roles = None, from_secondary = True):
		if roles and 'developer' in roles:
			collection += '_developer'
		elif roles and 'researcher' in roles:
			collection += '_researcher'

		db = self.getDatabase(collection)

		if from_secondary and self.allow_secondary_reads:
			db.read_preference = pymongo.ReadPreference.SECONDARY_PREFERRED

		coll = db[collection]
		return coll.find(query, fields)
