"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from sensible_data_service.db_access.mysql_wrapper import DBWrapper


class TestWrapper(TestCase):
	def test_get_db_connection(self):
		test_database = "testdb"
		wrapper = DBWrapper()
		conn = wrapper.get_db_connection_for_probe(test_database)
		self.fail("Finish the test")