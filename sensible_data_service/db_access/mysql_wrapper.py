import MySQLdb as mdb
#import SECURE_settings
import time


class Wrapper:
	def __init__(self):
		self.read_hostname = "localhost"
		self.write_hostname = "localhost"
		self.username = 'radugatej'#SECURE_settings.DATA_DATABASE['username']
		self.password = 'Who.gon.stop.me'#SECURE_settings.DATA_DATABASE['password']
		self.open_databases = {}

	def get_read_db_connection_for_probe(self, probe):
		return self.get_db_connection_for_probe(probe, True)

	def get_write_db_connection_for_probe(self, probe):
		return self.get_db_connection_for_probe(probe, False)

	def get_connection_parameters_for_probe(self, probe):
		params = {}
		params['read_hostname'] = "localhost"#SECURE_settings.DATA_DATABASES[probe]['read_hostname']
		params['write_hostname'] = "localhost"#SECURE_settings.DATA_DATABASES[probe]['write_hostname']
		params['username'] = "radugatej"#SECURE_settings.DATA_DATABASES[probe]['username']
		params['password'] = "Who.gon.stop.me"#SECURE_settings.DATA_DATABASES[probe]['password']

		return params

	def get_db_connection_for_probe(self, probe, read_connection):

		database_name = probe
		connection = None
		if database_name in self.open_databases:
			return self.open_databases[database_name]
		else:
			connection_parameters = self.get_connection_parameters_for_probe(probe)
			hostname = None
			if read_connection:
				hostname = connection_parameters['read_hostname']
			else:
				hostname = connection_parameters['write_hostname']

			username = connection_parameters['username']
			password = connection_parameters['password']

			try:
				connection = mdb.connect(hostname, username, password, database_name)
				self.open_databases[database_name] = connection
			except mdb.Error, e:
				print "Error %d: %s" % (e.args[0], e.args[1])

		return connection

	def insert(self, rows, probe, user_role=None):
		connection = self.get_read_db_connection_for_probe(probe)
		table_name = self.get_table_name_for_db(user_role)
		for row in rows:
			self.insert_row(row, table_name, connection)
		connection.commit()

	def get_table_name_for_db(self, user_role):
		if user_role:
			return user_role
		else:
			return "main"

	def insert_row(self, row, table_name, connection):

		if not type(row['timestamp']) == str:
			row['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(row['timestamp']))
		if 'timestamp_added' in row and not type(row['timestamp_added']) == str:
			row['timestamp_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(row['timestamp_added']))

		query = 'INSERT IGNORE INTO ' + table_name + " ("
		query += ','.join(row.keys())
		query += ") VALUES ("
		query += ','.join(["%s" for x in row.keys()])
		query += ')'

		parameters = [row[x] for x in row.keys()]
		self.execute_query_on_db(query, connection, parameters=parameters)

	def execute_query_on_db(self, query, connection, parameters=None):
		cursor = connection.cursor()
		cursor.execute(query, parameters)
