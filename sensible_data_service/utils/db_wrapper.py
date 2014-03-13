from pymongo import MongoClient, MongoReplicaSetClient
import SECURE_settings
from django.conf import settings
import pymongo
from utils import database
from db_access import mysql_wrapper
from db_access import json_to_csv
import pdb
class DatabaseHelper:

	def __init__(self, engine = 'mysql'):
		if engine == 'mysql':
			self.engine = mysql_wrapper.DBWrapper()
		elif engine == 'mongo':
			self.engine = database.Database()
		else:
			raise ValueError(engine + ' is not a valid engine type')

	def insert(self, documents, collection, roles = None):
		probe = collection

		#TEMPORARY upload to both mongo AND mysql.

		#Mongo
		database.Database().insert(documents, collection, roles)

		if isinstance(documents, dict):
			documents = [documents]
		#MySQL
		if isinstance(self.engine, mysql_wrapper.DBWrapper):
			payload = []
			for document in documents:
				#pdb.set_trace()
				payload += json_to_csv.json_to_csv(document, probe)
			if 'facebook' in probe: probe = 'facebook'
			self.engine.insert(payload, probe, roles)
		# # if it's the mysql wrapper, the documents have to be transformed into lists of rows
		# if isinstance(self.engine, mysql_wrapper.DBWrapper):
		# 	payload = []
		# 	for document in documents:
		# 		#pdb.set_trace()
		# 		payload += json_to_csv.json_to_csv(document, probe)
		# 	if 'facebook' in probe: probe = 'facebook'
		# 	self.engine.insert(payload, probe, roles)
		# elif isinstance(self.engine, database.Database):
		# 	self.engine.insert(documents, collection, roles)
	
	""" 
	params: dictionary used to construct engine specific query. Keys:
	'sortby' - column to sort by (enforced to timestamp)
	'decrypted',
	'order', - +1 for ASCENDING, -1 for DESCENDING
	'fields', projection
	'start_date',minimum value of timestamp (inclusive)
	'end_date',maximum value of timestamp (inclusive)
	'limit',how many rows to pass
	'users',list of users
	'after', id of the last returned document, used for paging
	'where' list dictionaries with a field and value(s), for example: 
		params['where'] = [{'device_id':['devid1', 'devid2']},{'timestamp':123345}]
	"""
	# def retrieve(self, params, collection, roles = None, from_secondary = True):
	# 	return self.engine.retrieve(params, collection, roles)

	def update_device_info(self, device_info_document):
		if isinstance(self.engine, mysql_wrapper.DBWrapper):
			self.engine.update_device_info(device_info_document)

	def getDocuments(self, query, collection, roles = None, from_secondary = True):
		# data retrieval not yet implemented in mysql, switching to mongo if necessary
		if isinstance(self.engine, mysql_wrapper.Wrapper):
			self.engine = database.Database()
		return self.engine.getDocuments(query, collection, roles, from_secondary)

	#to be merged with getDocuments with default fields argument
	def getDocumentsCustom(self, query, collection, fields, roles = None, from_secondary = True):
		# data retrieval not yet implemented in mysql, switching to mongo if necessary
		if isinstance(self.engine, mysql_wrapper.Wrapper):
			self.engine = database.Database()
		return self.engine.getDocumentsCustom(query, collection, fields, roles, from_secondary)
