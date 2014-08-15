import base64
import json
from pymongo import MongoClient, MongoReplicaSetClient
import SECURE_settings
from django.conf import settings
import pymongo
from utils import database
from db_access import mysql_wrapper, filesystem_wrapper
from db_access import json_to_csv
from sensible_audit import audit

class DatabaseHelper:

	def __init__(self, engine = 'mysql'):
		self.log = audit.getLogger(__name__)
		if engine == 'mysql':
			self.engine = mysql_wrapper.DBWrapper()
			self.filestorage_wrapper = filesystem_wrapper.FileSystemWrapper()
		elif engine == 'mongo':
			self.engine = database.Database()
		else:
			raise ValueError(engine + ' is not a valid engine type')

	def insert(self, documents, collection, roles = None):
		probe = collection

		if isinstance(documents, dict):
			documents = [documents]
		#MySQL
		if isinstance(self.engine, mysql_wrapper.DBWrapper):
			payload = []
			try:
				for document in documents:
					payload += json_to_csv.json_to_csv(document, probe)
				self.engine.insert(payload, probe, roles)
			except Exception, e: 
				self.log.error({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})

			try:
				self.filestorage_wrapper.insert(documents, probe, roles)
			except Exception, e:
				self.log.error({'type': 'FileStorage', 'tag': 'insert', 'exception': str(e)})
		


	def insert_rows(self, rows, collection, roles = None):
		try:
			if not rows:
				self.log.debug({'type': 'MYSQL', 'tag': 'insert', 'message': "No rows to insert"})
				return
			self.engine.insert(rows, collection, roles)
		except Exception, e:
			self.log.error({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})


	def retrieve(self, params, collection, roles = None):
		"""params: dictionary used to construct engine specific query. Keys:
			'sortby' - column to sort by (enforced to timestamp)
			'decrypted',
			'order', - +1 for ASCENDING, -1 for DESCENDING
			'fields', projection
			'start_date',minimum value of timestamp (inclusive)
			'end_date',maximum value of timestamp (inclusive)
			'limit',how many rows to pass
			'users',list of users
			'after', id of the last returned document, used for paging
			'where', constraints on the query; so far only '..where column = ['value 1', 'value 2', ..] type constraints are supported
			'bearer_token', uniquely identifies the user, passed on solely
							for handling query paging
			"""
		if 'facebook' in collection:
			print collection
			facebook_data_type = collection.split("_")[4]
			params['where'] = {"data_type": [facebook_data_type]}
		results = self.engine.retrieve(params, collection, roles)
		if isinstance(self.engine, mysql_wrapper.DBWrapper):
			if 'facebook' in collection:
				for result in results:
					result['data'] = json.loads(base64.b64decode(result['data']))
		return results

	def update_device_info(self, device_info_document):
		if isinstance(self.engine, mysql_wrapper.DBWrapper):
			self.engine.update_device_info(device_info_document)

        def execute_named_query(self, named_query, params, readonly=True):
                if isinstance(self.engine, mysql_wrapper.DBWrapper):
                        if readonly:
                                connection = self.engine.get_read_db_connection_for_probe(named_query["database"])
                        else:
                                connection = self.engine.get_write_db_connection_for_probe(named_query["database"])
                        cur = self.engine.execute_query_on_db(named_query["query"], connection, params)
                        if not readonly:
                                connection.commit()
                        return cur
