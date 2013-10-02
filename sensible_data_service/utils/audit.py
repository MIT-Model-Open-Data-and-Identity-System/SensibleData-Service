from pymongo import MongoClient
import datetime
import json
import time
import shutil
import SECURE_settings
from django.conf import settings
from utils import log

class Audit:
	client = None
	db = None

	def __init__(self):
		self.client = MongoClient(settings.AUDIT_DATABASE['params']['url']%(SECURE_settings.AUDIT_DATABASE['username'],SECURE_settings.AUDIT_DATABASE['password']))
		self.db = self.client[settings.AUDIT_DATABASE['params']['database']]
	
	def copyToFile(self, severity, typ, doc):
		doc['type']=typ
		log.log(severity,json.dumps(doc))

	def decision(self, severity,typ,tag,doc):
		if severity=='ERROR': return True
		else: return False	

	def log(self, severity, typ, tag, doc):
		doc['TIMESTAMP']=str(datetime.datetime.now()) 
		doc['tag']= tag
		doc['severity']= severity
		coll = self.db[typ]
		doc_id=coll.insert(doc, continue_on_error=True)

		if self.decision(severity,typ,tag,doc): self.copyToFile(severity, typ, doc)

	def d(self, typ, tag, doc):
		self.log('DEBUG', typ, tag, doc)
		
	def w(self, typ, tag, doc):
		self.log('WARNING', typ, tag, doc)

	def e(self, typ, tag, doc):
		self.log('ERROR', typ, tag, doc)
