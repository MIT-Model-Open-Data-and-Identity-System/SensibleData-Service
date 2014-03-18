import json
import itertools
from django.conf import settings
from nose_parameterized import parameterized
from sensible_data_service.db_access.json_to_csv import json_to_csv
from sensible_data_service.db_access.mysql_wrapper import DBWrapper
from sensible_data_service.db_access.tests.base import TestMySQLWrapper, load_parameters_for_dbs_and_tables, PROBE_NAMES
import MySQLdb as mdb
from sensible_data_service.sensible_data_service import LOCAL_SETTINGS
from sensible_data_service.utils import SECURE_settings


class TestDBPopulation(TestMySQLWrapper):

	def __init_test_connection(self, probe):
		database = settings.DATA_DATABASE_SQL["DATABASES"][probe]
		test_connection = mdb.connect(settings.DATA_DATABASE_SQL["READ_HOST"], SECURE_settings.DATA_DATABASE_SQL["username"], SECURE_settings.DATA_DATABASE_SQL["password"], database)
		test_connection.autocommit(True)
		self.test_connection = test_connection

	@parameterized.expand(load_parameters_for_dbs_and_tables())
	def test_insert_unique(self, name, probe, table_name):
		self.__init_test_connection(probe)

		test_cursor = self.test_connection.cursor()
		test_cursor.execute("truncate table " + table_name)

		test_cursor.execute("select count(*) from " + table_name)
		items_before = test_cursor.fetchall()[0][0]

		test_documents = self.__get_test_data_for_probe(probe)

		wrapper = DBWrapper()
		wrapper.insert(test_documents, probe, None if table_name == 'main' else table_name)

		test_cursor = self.test_connection.cursor()
		test_cursor.execute("select count(*) from " + table_name)
		items_after = test_cursor.fetchall()[0][0]

		self.assertNotEqual(items_before, items_after)
		self.assertEquals(items_after - items_before, len(test_documents))

	@parameterized.expand(load_parameters_for_dbs_and_tables())
	def test_insert_duplicates(self, name, probe, table_name):
		if "facebook" in probe:
			return
		self.__init_test_connection(probe)
		test_cursor = self.test_connection.cursor()
		test_cursor.execute("truncate table " + table_name)
		test_cursor.execute("select count(*) from " + table_name)
		items_before = test_cursor.fetchall()[0][0]

		test_documents = self.__get_test_data_for_probe(probe)

		wrapper = DBWrapper()
		wrapper.insert([test_documents[0], test_documents[0]], probe, None if table_name == 'main' else table_name)

		test_cursor = self.test_connection.cursor()
		test_cursor.execute("select count(*) from " + table_name)
		items_after = test_cursor.fetchall()[0][0]

		self.assertEquals(items_after - items_before, 1)

	def __get_test_data_for_probe(self, probe):
		test_file = open(settings.ROOT_DIR  + "/db_access/tests/test_data/" + probe + ".json")
		return list(itertools.chain.from_iterable([json_to_csv(json.loads(line), probe) for line in test_file]))