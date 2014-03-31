from django.conf import settings
from django.core.management import BaseCommand
from pymongo import MongoClient
from db_access import json_to_csv
from db_access.filesystem_wrapper import FileSystemWrapper
from db_access.mysql_wrapper import DBWrapper
from utils import SECURE_settings
from sensible_audit import audit


class Command(BaseCommand):
	# def __init__(self):
	# 	self.log = audit.getLogger(__name__)

	def handle(self, *args, **options):
		print args

		probe = args[0]
		roles = args[1]

		username = SECURE_settings.DATA_DATABASE["username"]
		password = SECURE_settings.DATA_DATABASE["password"]
		host = settings.DATA_DATABASE["nodes"][0]

		client = MongoClient('mongodb://%s:%s@%s/admin'%(username, password, host), ssl=True)
		collection = client[settings.DATA_DATABASE["available_databases"]][probe + "_" + roles]

		counter = 0
		mysql_wrapper = DBWrapper()
		filestorage_wrapper = FileSystemWrapper()

		payload = []
		for document in collection:
			try:
				payload += json_to_csv.json_to_csv(document, probe)
				filestorage_wrapper.insert([document], probe, roles)
				counter += 1
			except Exception, e: print e

			if counter % 1000 == 0:
				try:
					mysql_wrapper.insert(payload, probe, roles)
				except Exception, e:
					print e# self.log.e({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})
				payload = []