import MySQLdb as mdb


class Wrapper:
	def _init_(self):
		self.hostname = ""
		self.username = ""
		self.password = ""

	def get_db_connection(self, database):
		hostname = self.hostname
		username = self.username
		password = self.password
		connection = None
		try:
			connection = mdb.connect(hostname, username, password, database)
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])

		return connection

	def insert_row(self, row, database):
		connection = self.get_db_connection(database)
		table_name = self.get_table_name_for_db()

		query = "INSERT IGNORE INTO " + table_name +  "("
		query += ','.join(row.keys())
		query += ") VALUES ("
		query += ','.join([str(row[x] for x in row.keys())])
		query += ')'

		self.execute_query_on_db(query, connection)
		connection.commit()

	def execute_query_on_db(self, query, connection):
		cursor = connection.cursor()
		cursor.execute(query)

	def get_table_name_for_db(self):
		return "table_name"



