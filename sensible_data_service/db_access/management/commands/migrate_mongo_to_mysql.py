from django.conf import settings
from django.core.management import BaseCommand
from pymongo import MongoClient
from db_access import json_to_csv
from db_access.filesystem_wrapper import FileSystemWrapper
from db_access.mysql_wrapper import DBWrapper
from utils import SECURE_settings
from sensible_audit import audit
import sys

BULK_SIZE = 200
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
			else:
				role = args[1]

		username = "radugatej"#SECURE_settings.DATA_DATABASE["username"]
		password = "kdbgaCQgCPJ4uFxLA6RA"#SECURE_settings.DATA_DATABASE["password"]
		host = settings.DATA_DATABASE["nodes"][0]
		database = "admin"
		client = MongoClient('mongodb://%s:%s@%s/%s'%(username, password, host, database), ssl=True)
		print "connected"
		collection_name = probe + "_" + role if not role == None else probe
		database_name = settings.DATA_DATABASE["available_databases"].get(probe, "sensibledtu_1k")
		collection = client[database_name][collection_name]
		print "after collection"
		sys.stdout.flush()
		counter = 0
		mysql_wrapper = DBWrapper()
		#filestorage_wrapper = FileSystemWrapper()
		connection = mysql_wrapper.get_write_db_connection_for_probe(probe)
		payload = []
		print collection.find().count()
		for document in collection.find():
			try:
				payload += json_to_csv.json_to_csv(document, probe)
				#filestorage_wrapper.insert([document], probe, role)
				counter += 1
			except Exception, e: 
				print repr(e)
				sys.stdout.flush()

			if counter % BULK_SIZE == 0:
				try:
					mysql_wrapper.insert_for_connection(connection, payload, probe, role)
					print "comitted"
				except Exception, e:
					print repr(e)# self.log.e({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})
					sys.stdout.flush()
				payload = []
		if len(payload) > 0:
			try:
				mysql_wrapper.insert_for_connection(connection, payload, probe, role)
                                print "comitted"
                        except Exception, e:
                                print repr(e)# self.log.e({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})
		connection.commit()
		connection.close()
