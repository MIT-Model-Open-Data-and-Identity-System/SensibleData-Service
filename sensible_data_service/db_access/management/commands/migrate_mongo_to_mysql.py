from django.conf import settings
from django.core.management import BaseCommand
from pymongo import MongoClient, MongoReplicaSetClient
from db_access import json_to_csv
from db_access.filesystem_wrapper import FileSystemWrapper
from db_access.mysql_wrapper import DBWrapper
from utils import SECURE_settings
from sensible_audit import audit
import sys
import time

BULK_SIZE = 10000
class Command(BaseCommand):
	# def __init__(self):
	# 	self.log = audit.getLogger(__name__)

	def handle(self, *args, **options):
		roles = ["researcher", "developer"]
		probe = args[0]
		role = None
		if len(args) > 1:
			if args[1] not in roles:
				raise BaseException("incorrect role")
			else:
				role = args[1]

		log_file = open("migrate_log", "a")
		log_file.write("Start: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n")
		log_file.flush()
		username = SECURE_settings.DATA_DATABASE["username"]
		password = SECURE_settings.DATA_DATABASE["password"]
		host = settings.DATA_DATABASE["nodes"][0]
		database = "admin"
		client = MongoReplicaSetClient('mongodb://%s:%s@%s/%s'%(username, password, host, database), ssl=True, replicaSet="sensibledtu")
		log_file.write("Connected to mongo" + "\n")
		log_file.flush()
		collection_name = probe + "_" + role if not role == None else probe
		database_name = settings.DATA_DATABASE["available_databases"].get(collection_name, "sensibledtu_1k")
		collection = client[database_name][collection_name]
		log_file.write("Collection: " + str(collection) + "\n")
		log_file.flush()
		counter = 0
		mysql_wrapper = DBWrapper()
		#filestorage_wrapper = FileSystemWrapper()
		connection = mysql_wrapper.get_write_db_connection_for_probe(probe)
		cursor = connection.cursor()
		payload = []
		log_file.write("No. of mongo documents: " + str(collection.find().count()) + "\n")
		mongo_cursor = collection.find().sort("timestamp_added", 1)
		for document in mongo_cursor:
			try:
				payload += json_to_csv.json_to_csv(document, probe)
				#filestorage_wrapper.insert([document], probe, role)
				counter += 1
			except Exception, e: 
				log_file.write(repr(e) + "\n")
				log_file.flush()

			if counter % BULK_SIZE == 0:
				try:
					mysql_wrapper.insert_for_connection(connection, payload, probe, role)
					log_file.write("Commited: " + str(counter) + " "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " + str(len(payload)) + " rows inserted" + "\n")
					log_file.flush() 
				except Exception, e:
					log_file.write(repr(e) + "\n")# self.log.e({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})
					log_file.flush()
				payload = []
		if len(payload) > 0:
			try:
				mysql_wrapper.insert_for_connection(connection, payload, probe, role)
                                log_file.write("Commited: " + str(counter) + " "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " " + str(len(payload)) + " rows inserted" + "\n")
				log_file.flush()
                        except Exception, e:
                                log_file.write(repr(e) + "\n")# self.log.e({'type': 'MYSQL', 'tag': 'insert', 'exception': str(e)})
				log_file.flush()
		connection.commit()
		connection.close()
		log_file.write("End: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "\n")
		log_file.flush()
		log_file.close()
