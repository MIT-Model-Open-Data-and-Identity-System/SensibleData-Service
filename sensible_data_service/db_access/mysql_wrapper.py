import MySQLdb as mdb
#import SECURE_settings
import time
import pdb

class DBWrapper:
	def __init__(self):
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
		#pdb.set_trace()
		connection = self.get_write_db_connection_for_probe(probe)
		table_name = self.get_table_name_for_db(user_role)
		#pdb.set_trace()
		for row in rows:
			self.insert_row(row, table_name, connection)
		connection.commit()

	def get_table_name_for_db(self, user_role):
		if user_role:
			if 'researcher' in user_role:
				return 'researcher'
			elif 'developer' in user_role:
				return 'developer'

		return "main"

	def insert_row(self, row, table_name, connection):
		#pdb.set_trace()
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
		#pdb.set_trace()
		cursor = connection.cursor(mdb.cursors.DictCursor)
		cursor.execute(query, parameters)
		return cursor

	def retrieve(self, params, probe, user_role):

		if "fields" not in params:
			params["fields"] = ["*"]
		table_name = self.get_table_name_for_db(user_role)
		self.check_columns_valid_for_table(params["fields"], probe, table_name)
		if "order" in params:
			order = self.get_order_from_param(params["order"])

		start_date = None
		if "start_date" in params:
			start_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(params['start_date']))

		end_date = None
		if "end_date" in params:
			end_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(params['end_date']))

		users = None
		if "users" in params:
			users = params['users']
			for i in range(0, len(users)):
				users[i] = "'" + users[i] + "'"

		where_clauses = []
		#where_clauses.append("timestamp BETWEEN " + "'" + start_date + "' AND '" + end_date + "'")
		#where_clauses.append("user IN " + "(" + ",".join(users) + ")")
		if "where" in params:
			for clause in params["where"]:
				clause_string = clause.keys()[0]

				if len(clause.values()[0]) > 1:
					clause_string += " IN"
					clause_string += "(" + ",".join(clause.values()[0]) + ")"
				else:
					clause_string += " ="
					clause_string += " '" + clause.values()[0] + "'"
				where_clauses.append(clause_string)

		query = "SELECT " + ",".join(params["fields"]) + " FROM " + table_name

		if len(where_clauses) > 0:
			where_clauses_string = " AND ".join(where_clauses)
			query += " WHERE "
			query += where_clauses_string

		if "sortby" in params:
			query += " ORDER BY " + params["sortby"] + " " + order

		if "limit" in params:
			query += " LIMIT 0," + str(params["limit"])

		print query
		connection = self.get_read_db_connection_for_probe(probe)
		return self.execute_query_on_db(query, connection, params)

	def get_order_from_param(self, param):
		if param == 1:
			return " "
		elif param == -1:
			return "DESC"

	def check_columns_valid_for_table(self, columns, probe, table_name):
		if "*" in columns:
			return
		connection = self.get_read_db_connection_for_probe(probe)
		cursor = connection.cursor()
		cursor.execute("SHOW COLUMNS from " + table_name)
		correct_columns = cursor.fetchall()
		correct_columns = [x[0] for x in correct_columns]
		invalid_columns = []
		for column in columns:
			if column not in correct_columns:
				invalid_columns.append(column)

		if len(invalid_columns) > 0:
			raise BaseException("Fields " + ",".join(invalid_columns) + " are not correct")


wrapper = DBWrapper()
params = {}
#params["fields"] = ["timestamp", "user"]
#params["sortby"] = "timestamp"
#params["order"] = 1
#params["start_date"] = 1391601999
#params["end_date"] = 1391602120
#params["users"] = ["dummarek"]
#params["limit"] = 2
#params["where"] = []#{'bssid':'7c:05:07:55:8d:4d'}, {'device_id':'a4574141ed7516c0dfe7e96bdc52b1'}]

cursor = wrapper.retrieve(params, "edu_mit_media_funf_probe_builtin_WifiProbe", None)
print cursor.fetchall()