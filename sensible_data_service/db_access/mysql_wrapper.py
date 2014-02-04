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

	def get_db_connection_for_probe(self, probe, read_connection):

		database_name = probe
		connection = None
		if database_name in self.open_databases:
			return self.open_databases[database_name]
		else:

			hostname = None

			if read_connection:
				hostname = self.read_hostname
			else:
				hostname = self.write_hostname

			username = self.username
			password = self.password

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

		print query
		parameters = [row[x] for x in row.keys()]
		print parameters
		self.execute_query_on_db(query, connection, parameters=parameters)

	def execute_query_on_db(self, query, connection, parameters=None):
		cursor = connection.cursor()
		cursor.execute(query, parameters)


wrapper = Wrapper()
row = {}
row['facebook_id'] = '1ac8a623b24d010d42529016c4b49a8f'
row['timestamp'] = 1376438853
row['user'] = '6d7363df17881d4afef71897a74840'
row['data'] = 'blablabablal'

row2 = {}
row2['facebook_id'] = '1ac8a623b24d010d42529016c4b49a8f'
row2['timestamp'] = 1376438853
row2['user'] = '6d7363df17881d4afef71897a74840'
row2['data'] = 'blablabablal'

rows = []
rows.append(row)
rows.append(row2)

wrapper.insert(rows, 'facebook')


