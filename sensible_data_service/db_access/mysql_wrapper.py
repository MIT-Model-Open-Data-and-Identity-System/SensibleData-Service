import MySQLdb as mdb
import SECURE_settings

class Wrapper:
	def __init__(self):
		self.read_hostname = "localhost"
		self.write_hostname = "localhost"
		self.username = SECURE_settings.DATA_DATABASE['username']
		self.password = SECURE_settings.DATA_DATABASE['password']
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

	def insert(self, rows, probe, user_role):
		connection = self.get_read_db_connection_for_probe(probe)
		table_name = self.get_table_name_for_db(user_role)
		cursor = connection.cursor()
		for row in rows:
			self.insert_row(row, cursor, table_name)
		connection.commit()

	def get_table_name_for_db(self, user_role):
		if user_role:
			return user_role
		else:
			return "main"

	def insert_row(self, row, table_name, connection):

		query = "INSERT IGNORE INTO " + table_name + "("
		query += ','.join(row.keys())
		query += ") VALUES ("
		query += ','.join([str(row[x] for x in row.keys())])
		query += ')'

		self.execute_query_on_db(query, connection)

	def execute_query_on_db(self, query, connection):
		cursor = connection.cursor()
		cursor.execute(query)


