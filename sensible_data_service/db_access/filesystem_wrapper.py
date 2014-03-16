import json
import os
import time


class FileSystemWrapper:
	def insert(self, documents, probe, role):
		for document in documents:
			self.store_document_on_file_server(document, probe, role)

	def store_document_on_file_server(self, document, probe, role):
		user = document['user']
		day = time.strftime('%Y-%m-%d', time.gmtime(row['timestamp']))
		filename = document['_id']
		with open(filename, 'w') as outfile:
			json.dump(document, outfile)

		os.system(
			"rsync -azvhe ssh " + filename + " root@162.243.64.42:/home/superlists/file_storage/" + probe + "/" + role + "/")


wrapper = FileSystemWrapper()

row = {}
row["_id"] = "sada"
row['timestamp'] = 1376414693
row['data'] = "blabla"
row['facebook_id'] = '1ac8a623b24d010d42529016c4b49a8f'
row['user'] = '6d7363df17881d4afef71897a74840'

wrapper.insert([row], 'facebook', "main")
