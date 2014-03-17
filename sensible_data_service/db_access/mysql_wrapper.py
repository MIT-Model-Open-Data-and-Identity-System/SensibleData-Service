import hashlib
from operator import itemgetter
import MySQLdb as mdb
#import SECURE_settings
import time
from django.conf import settings
from utils import SECURE_settings
from sensible_audit import audit
import json

class DBWrapper:

	def get_read_db_connection_for_probe(self, probe):
		return self.get_db_connection_for_probe(probe, True)

	def get_write_db_connection_for_probe(self, probe):
		return self.get_db_connection_for_probe(probe, False)

	def __get_connection_parameters(self, probe, is_read_connection):
		params = {}
		params['hostname'] = settings.DATA_DATABASE_SQL["READ_HOST"] if is_read_connection else settings.DATA_DATABASE_SQL["WRITE_HOST"]
		params['username'] = SECURE_settings.DATA_DATABASE_SQL['username']
		params['password'] = SECURE_settings.DATA_DATABASE_SQL['password']
		params['ssl'] = SECURE_settings.DATA_DATABASE_SQL['ssl']

		return params

	def get_db_connection_for_probe(self, probe, is_read_connection):

		database_name = settings.DATA_DATABASE_SQL["DATABASES"][probe]

		connection = None

		#TODO: Get proper connection pooling
		connection_parameters = self.__get_connection_parameters(probe, is_read_connection)
		hostname = connection_parameters['hostname']
		username = connection_parameters['username']
		password = connection_parameters['password']
		ssl = connection_parameters['ssl']

		try:
			connection = mdb.connect(hostname, username, password, database_name, ssl=ssl, charset="utf8", use_unicode=True)
		except mdb.Error, e:
			audit.Audit().e("MySQL", "connect", {"exception": str(e)})

		return connection

	def insert(self, rows, probe, user_role=None):
		connection = self.get_write_db_connection_for_probe(probe)
		table_name = self.__get_table_name(user_role, probe)
		row_max_len, row = max([(len(row.keys()), row) for row in rows], key=itemgetter(0))

		insert_query = self.__get_insert_query(table_name, row.keys())

		values_to_insert = self.__get_values_to_insert(rows, row.keys())
		cursor = connection.cursor()
		cursor.executemany(insert_query, values_to_insert)
		connection.commit()
	
	#Notice the small (as in non-capital) letters used for
	#the query. The query is much slower with capital letters
	#for some very weird reason. 
	def __get_insert_query(self, table_name, keys):
		query = 'insert ignore into ' + table_name + " ("
		query += ','.join(keys)
		query += ") values("
		query += ','.join(["%s" for x in keys])
		query += ')'

		return query

	def __get_values_to_insert(self, rows, keys):
		insert_values = []
		for row in rows:
			if not row: continue
			if type(row['timestamp']) in [float, int]:
				row['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['timestamp']))
			if 'timestamp_added' in row and not type(row['timestamp_added']) == str:
				row['timestamp_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['timestamp_added']))

			insert_values.append(tuple([row.get(x) for x in keys]))

		return insert_values

	def __get_table_name(self, user_role, probe):
		if user_role:
			if 'researcher' in user_role:
				return 'researcher'
			elif 'developer' in user_role:
				return 'developer'

		if probe == "device_inventory":
			return "device_inventory"

		return "main"

	def execute_query_on_db(self, query, connection, parameters=None):
		cursor = connection.cursor(mdb.cursors.DictCursor)
		cursor.execute(query, parameters)
		return cursor

	def update_device_info(self, device_info_document):
		connection = self.get_write_db_connection_for_probe("common_admin")
		query = 'INSERT INTO ' + "device_inventory" + " ("
		query += ','.join(device_info_document.keys())
		query += ") VALUES ("
		query += ','.join(["%s" for x in device_info_document.keys()])
		query += ')'
		update_keys = [str(x) + "=values(" + str(x) + ")" for x in device_info_document.keys()]
		query += "ON DUPLICATE KEY UPDATE " + ','.join(update_keys)

		parameters = [device_info_document[x] for x in device_info_document.keys()]
		self.execute_query_on_db(query, connection, parameters=parameters)
		connection.commit()

