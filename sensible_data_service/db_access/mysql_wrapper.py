import hashlib
import MySQLdb as mdb
#import SECURE_settings
import time
from django.conf import settings
from sensible_data_service.utils import SECURE_settings


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
			connection = mdb.connect(hostname, username, password, database_name, ssl=ssl)
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

		return connection

	def insert(self, rows, probe, user_role=None):
		connection = self.get_write_db_connection_for_probe(probe)
		table_name = self.__get_table_name(user_role, probe)
		for row in rows:
			if not row: continue
			self.insert_row(row, table_name, connection)
		connection.commit()

	def __get_table_name(self, user_role, probe):
		if user_role:
			if 'researcher' in user_role:
				return 'researcher'
			elif 'developer' in user_role:
				return 'developer'

		if probe == "device_inventory":
			return "device_inventory"

		return "main"

	def insert_row(self, row, table_name, connection):
		if type(row['timestamp']) in [float, int]:
			row['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['timestamp']))
		if 'timestamp_added' in row and not type(row['timestamp_added']) == str:
			row['timestamp_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['timestamp_added']))

		query = 'INSERT IGNORE INTO ' + table_name + " ("
		query += ','.join(row.keys())
		query += ") VALUES ("
		query += ','.join(["%s" for x in row.keys()])
		query += ')'

		parameters = [row[x] for x in row.keys()]
		self.execute_query_on_db(query, connection, parameters=parameters)

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