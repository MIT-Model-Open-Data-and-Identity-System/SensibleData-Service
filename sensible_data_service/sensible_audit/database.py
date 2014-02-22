from bson.timestamp import Timestamp
from pymongo import Connection
from pymongo.collection import Collection
from pymongo.errors import OperationFailure, PyMongoError
import SECURE_settings

class AuditDB:

	def __init__(self, **options):
		self.database_name = SECURE_settings.AUDIT_DATABASE['DATABASE']
		self.host = SECURE_settings.AUDIT_DATABASE['HOST']
		self.port = SECURE_settings.AUDIT_DATABASE['PORT']
		self.username = SECURE_settings.AUDIT_DATABASE['USERNAME']
		self.password = SECURE_settings.AUDIT_DATABASE['PASSWORD']
		self.collection_name = SECURE_settings.AUDIT_DATABASE['COLLECTION']
		self.options = options
		self._connect()

	def _connect(self):
		"""
		Connect to the mongodb database
		"""
		try:
			self.connection = Connection(host=self.host, port=self.port, **self.options)
		except PyMongoError:
			raise
		
		self.database = self.connection[self.database_name]
		if self.username is not None and self.password is not None:
			self.authenticated = self.database.authenticate(self.username, self.password)
		self.collection = self.database[self.collection_name]

	def documents(self, query):
		return self.collection.find()

	def close(self):
		if self.authenticated:
			self.database.logout()
		if self.connection is not None:
			self.connection.disconnect()

