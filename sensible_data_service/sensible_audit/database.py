from pymongo import MongoClient
from utils import SECURE_settings
from django.conf import settings

class Database:
	client = None
	db = None

	def __init__(self):
		self.initDB()


	def initDB(self):
		if self.client and self.db: return

		try: self.is_replica_set = settings.AUDIT_DATABASE['is_replica_set']
		except KeyError: self.is_replica_set = False

		try: self.replica_set = settings.AUDIT_DATABASE['replica_set']
		except KeyError: self.replica_set = ""

		try: self.ssl = settings.AUDIT_DATABASE['ssl']
		except KeyError: self.ssl = False

		try: self.allow_secondary_reads = settings.AUDIT_DATABASE['allow_secondary_reads']
		except KeyError: self.allow_secondary_reads = False

		self.nodes = settings.AUDIT_DATABASE['nodes']
		self.database = settings.AUDIT_DATABASE['database']

		if self.is_replica_set:
			self.client = MongoReplicaSetClient('mongodb://%s/%s'%(','.join(self.nodes), self.database), ssl=self.ssl, replicaSet=self.replica_set)
			self.db = self.client[settings.AUDIT_DATABASE['database']]
		else:
			self.client = MongoClient('mongodb://%s/%s'%(','.join(self.nodes), self.database), ssl=self.ssl)
			self.db = self.client[settings.AUDIT_DATABASE['database']]
			
			
		self.db.authenticate(SECURE_settings.AUDIT_DATABASE['username'],SECURE_settings.AUDIT_DATABASE['password'])

	def insert(self, doc, collection):
		coll = self.db[collection]
		doc_id = coll.insert(doc, continue_on_error=True)
		return doc_id
