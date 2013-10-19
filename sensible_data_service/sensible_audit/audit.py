from pymongo import MongoClient
import bson.json_util as json
import time
import shutil

from utils import SECURE_settings
from django.conf import settings
from utils import log

import conf

class Audit:
	client = None
	db = None

	def __init__(self):
		pass
	
	def copyToFile(self, severity, type, doc):
		doc['type']=type
		log.log(severity,json.dumps(doc))

	def shouldCopyToFile(self, severity, type, tag, doc):
		if severity=='ERROR': return True
		else: return False	

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





	def log(self, severity, type, tag, doc, onlyfile):
		if onlyfile:
			 self.copyToFile(severity, type, doc)
		else:
			self.initDB()
			doc['TIMESTAMP']= time.time()
			doc['tag']= tag
			doc['severity']= severity
			coll = self.db[type]
			doc_id=coll.insert(doc, continue_on_error=True)

			if self.shouldCopyToFile(severity,type,tag,doc): self.copyToFile(severity, type, doc)

	def d(self, type, tag, doc, onlyfile=False):
		self.log('DEBUG', type, tag, doc, onlyfile)
		
	def w(self, type, tag, doc, onlyfile=False):
		self.log('WARNING', type, tag, doc, onlyfile)

	def e(self, type, tag, doc, onlyfile=False):
		self.log('ERROR', type, tag, doc, onlyfile)
