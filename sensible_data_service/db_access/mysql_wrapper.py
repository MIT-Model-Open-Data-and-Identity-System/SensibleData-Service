import hashlib
from operator import itemgetter
import MySQLdb as mdb
#import SECURE_settings
import time
from django.conf import settings
from db_access import PROBE_SETTINGS
from django.core.cache import cache, get_cache
from utils import SECURE_settings
from sensible_audit import audit
import json

class DBWrapper:

	def __init__(self):
		self.log = audit.getLogger(__name__)
		self.cache = get_cache("memory")

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
			self.log.error({'type': 'MYSQL', 'tag': 'connect', 'exception': str(e)})

		return connection

	def insert(self, rows, probe, user_role=None):
		connection = self.get_write_db_connection_for_probe(probe)
		table_name = self.__get_table_name(user_role, probe)
		row_max_len, row = max([(len(row.keys()), row) for row in rows], key=itemgetter(0))
		keys = row.keys()
		keys.append("uniqueness_hash")
		insert_query = self.__get_insert_query(table_name, keys)

		values_to_insert = self.get_values_to_insert(rows, keys, PROBE_SETTINGS.UNIQUE_FIELDS[settings.DATA_DATABASE_SQL["DATABASES"][probe]])
		cursor = connection.cursor()
		try:
			cursor.executemany(insert_query, values_to_insert)
		except mdb.Error, e:
			if "Deadlock" in str(e):
				cursor.executemany(insert_query, values_to_insert)
			else:
				self.log.error({'type': 'MYSQL', 'tag': 'executemany', 'exception': str(e)})
		connection.commit()

	def insert_for_connection(self, connection, rows, probe, user_role=None):
		table_name = self.__get_table_name(user_role, probe)
                row_max_len, row = max([(len(row.keys()), row) for row in rows], key=itemgetter(0))
		keys = row.keys()
                keys.append("uniqueness_hash")
                insert_query = self.__get_insert_query(table_name, keys)

                values_to_insert = self.get_values_to_insert(rows, keys, PROBE_SETTINGS.UNIQUE_FIELDS[settings.DATA_DATABASE_SQL["DATABASES"][probe]])
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

	def get_values_to_insert(self, rows, keys, unique_keys):
		insert_values = []
		for row in rows:
			if not row: continue
			if type(row['timestamp']) in [float, int]:
				row['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['timestamp']))
			if 'timestamp_added' in row and not type(row['timestamp_added']) == str:
				row['timestamp_added'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['timestamp_added']))
			if unique_keys:
				row["uniqueness_hash"] = hashlib.sha1("".join(str(row[unique_key]) for unique_key in unique_keys)).digest()
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

	def retrieve(self, params, probe, user_role):
		if params == None:
			return
		table_name = self.__get_table_name(user_role, probe)
		self.__check_columns_valid_for_table(params, probe, table_name)

		#In order to keep paged queries consistent between each other,
		#the results are limited by the max id of the table at the time
		#of the initial query

		extra_constraints = []
		max_id_constraint = self.__get_max_id_constraint(params, table_name, probe)
		if max_id_constraint: extra_constraints.append(max_id_constraint)
		where_query_string, where_query_params = self.__where(params, extra_constraints)

		query = "select " + ",".join(params.get("fields", ["*"])) + " from " + table_name
		query += where_query_string
		query += self.__sortby(params)
		query += self.__order(params)
		query += self.__limit(params)

		print query
		connection = self.get_read_db_connection_for_probe(probe)
		return self.execute_query_on_db(query, connection, where_query_params)

	def __limit(self, params):
		limit = params.get("limit", -1)
		try: limit = int(limit)
		except: limit = -1
		try: page_number = int(params.get("after", 0))
		except: page_number = 0
		if limit < 0:
			return ""
		return " limit " + str(page_number * limit) + ", " + str(limit)

	def __order(self, params):
		if not params.get("sortby"):
			return ""
		order = params.get("order", 0)
		if order == 1:
			return " " + "asc"
		elif order == -1:
			return " " + "desc"
		return ""

	def __sortby(self, params):
		if params.get("sortby"):
			return " order by " + params.get("sortby", "")
		return ""

	def __where(self, params, constraints=None):
		if constraints is None:
			constraints = []
		time_constraints = self.__get_time_constraint(params)
		if time_constraints: constraints.append(time_constraints)

		user_constraints = self.__get_user_constraint(params)
		if user_constraints: constraints.append(user_constraints)

		specific_constraints = self.__get_specific_constraints(params)
		if specific_constraints: constraints.extend(specific_constraints)

		if not constraints:
			return "", None
		where_clauses_params = []
		where_clause_strings = []
		for constraint in constraints:
			where_clause_strings.append(constraint["query_string"])
			where_clauses_params.extend(constraint["query_params"])
		where_clauses_string = " and ".join(where_clause_strings)
		where_clauses_params = tuple(where_clauses_params)
		return " " + "where " + where_clauses_string, where_clauses_params

	def __get_max_id_constraint(self, params, table_name, probe):
		query_key = hashlib.sha256(','.join([str(params[key]) for key in params.keys() if not key == "after"]) + probe + table_name).hexdigest()
		if params.get("after", 0) == 0:
			max_id = self.__get_table_max_id(table_name, probe)
			self.cache.set(query_key, max_id)
			return None

		max_id = self.cache.get(query_key)
		if not max_id:
			max_id = self.__get_table_max_id(table_name, probe)
			self.cache.set(query_key, max_id)
		return {"query_string": " id <= %s", "query_params": [max_id]}

	def __get_table_max_id(self, table_name, probe):
		connection = self.get_read_db_connection_for_probe(probe)
		return self.execute_query_on_db("select max(id) from " + table_name, connection).fetchall()[0]["max(id)"]

	def __get_specific_constraints(self, params):
		query_formatted_constraints = []
		constraints = params.get("where", {})
		for constraint in constraints:
				query_formatted_constraints.append({"query_string": constraint + " = %s", "query_params": [str(constraints[constraint])]})

		return query_formatted_constraints

	def __check_columns_valid_for_table(self, params, probe, table_name):
		columns = list(params.get("fields", ["*"]))
		if "*" in columns:
			columns.remove("*")
		#check the sortby column as well
		if params.get("sortby"): columns.append(params.get("sortby"))
		connection = self.get_read_db_connection_for_probe(probe)
		cursor = connection.cursor()
		cursor.execute("show columns from " + table_name)
		correct_columns = cursor.fetchall()
		correct_columns = [x[0] for x in correct_columns]
		invalid_columns = []
		for column in columns:
			if column not in correct_columns:
				invalid_columns.append(column)

		if len(invalid_columns) > 0:
			raise BaseException("Fields " + ",".join(invalid_columns) + " are not correct")

	def __get_time_constraint(self, params):
		start_date = None
		if "start_date" in params and params["start_date"]:
			start_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(params['start_date']))

		end_date = None
		if "end_date" in params and params["end_date"]:
			end_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(params['end_date']))

		if start_date and end_date:
			return {"query_string": "timestamp BETWEEN %s AND %s", "query_params": [start_date, end_date]}
		elif start_date and not end_date:
			return {"query_string": "timestamp >= %s", "query_params": [start_date]}
		elif end_date and not start_date:
			return {"query_string": "timestamp < %s", "query_params": [end_date]}

		return ""

	def __get_user_constraint(self, params):
		users = params.get('users', [])
		print users
		print params
		if not type(users) is list:
			raise BaseException("Users parameter is incorrectly formatted: needs to be a list")
		query_formatted_usernames = ["%s" for u in users]
		if "all" not in users and len(query_formatted_usernames) > 0:
			return {"query_string": "user IN " + "(" + ",".join(query_formatted_usernames) + ")", "query_params": users}
		return ""

	def execute_query_on_db(self, query, connection, parameters=None):
		#self.log.d({"type": "MYSQL", "tag":"query", "query": query, "query_params": str(parameters) })
		cursor = connection.cursor(mdb.cursors.DictCursor)
		cursor.execute(query, parameters)
		return cursor

	def update_device_info(self, device_info_document):
		connection = self.get_write_db_connection_for_probe("common_admin")
		query = 'insert into ' + "device_inventory" + " ("
		query += ','.join(device_info_document.keys())
		query += ") values ("
		query += ','.join(["%s" for x in device_info_document.keys()])
		query += ')'
		update_keys = [str(x) + "=values(" + str(x) + ")" for x in device_info_document.keys()]
		query += "on duplicate key update " + ','.join(update_keys)

		parameters = [device_info_document[x] for x in device_info_document.keys()]
		self.execute_query_on_db(query, connection, parameters=parameters)
		connection.commit()