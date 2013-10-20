import bson.json_util as json
import time

import log
import database
import conf

class Audit:
	db = None

	def __init__(self):
		pass
	
	def copyToFile(self, severity, type, doc):
		doc['type']=type
		log.log(severity,json.dumps(doc))

	def shouldCopyToFile(self, severity, type, tag, doc):
		if severity=='ERROR': return True
		else: return False	

	def log(self, severity, type, tag, doc, onlyfile):
		if onlyfile:
			 self.copyToFile(severity, type, doc)
		else:
			self.db = database.Database()
			doc['TIMESTAMP']= time.time()
			doc['tag']= tag
			doc['severity']= severity
			self.db.insert(doc=doc, collection=type)
			if self.shouldCopyToFile(severity, type, tag, doc): self.copyToFile(severity, type, doc)

	def d(self, type, tag, doc, onlyfile=True):
		self.log('DEBUG', type, tag, doc, onlyfile)
		
	def w(self, type, tag, doc, onlyfile=False):
		self.log('WARNING', type, tag, doc, onlyfile)

	def e(self, type, tag, doc, onlyfile=False):
		self.log('ERROR', type, tag, doc, onlyfile)
