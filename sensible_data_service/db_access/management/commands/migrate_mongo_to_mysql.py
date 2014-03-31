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
		roles = ["researcher", "developer"]
		probe = args[0]
		role = None
		if len(args) > 1:
			if args[1] not in roles:
				raise BaseException("incorrect role")

		username = SECURE_settings.DATA_DATABASE["username"]
		password = SECURE_settings.DATA_DATABASE["password"]
		host = settings.DATA_DATABASE["nodes"][0]

		client = MongoClient('mongodb://%s:%s@%s/admin'%(username, password, host), ssl=True)
		collection_name = probe + "_" + role if not role == None else probe
		collection = client[settings.DATA_DATABASE["available_databases"]][collection_name]

		counter = 0
		mysql_wrapper = DBWrapper()
		filestorage_wrapper = FileSystemWrapper()

		payload = []
		for document in collection.find():
			try:
				payload += json_to_csv.json_to_csv(document, probe)
				filestorage_wrapper.insert([document], probe, role)
				counter += 1
			except Exception, e: print repr(e)

			if counter % 1000 == 0:
				try:
					mysql_wrapper.insert(payload, probe, role)
					print "comitted"
				except Exception, e:
					print repr(e)# self.log.e({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})
				payload = []