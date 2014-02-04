"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from sensible_data_service.dao.wrapper import Wrapper


class TestWrapper(TestCase):
	def test_get_db_connection(self):
		test_database = "testdb"
		wrapper = Wrapper()
		conn = wrapper.get_db_connection(test_database)
		self.fail("Finish the test")