import json
from django.conf import settings
import os
import time
import shutil
import hashlib

class FileSystemWrapper:
	def insert(self, documents, probe, role):
		for document in documents:
			self.store_document_on_file_server(document, probe, role)

	def store_document_on_file_server(self, document, probe, role=None):
		if role == None or not 'researcher' in role or not "developer" in role:
			role = "main"
		user_dir = os.path.join(settings.FILESYSTEM_DATABASE["LOCAL_DIR"], probe, role, document['user'])
		doc_timestamp = time.mktime(time.strptime(document.get('last_answered')[:19],'%Y-%m-%d %H:%M:%S')) if "questionnaire" in probe else document['timestamp']
		filename = hashlib.sha1(json.dumps(document)).hexdigest()+'_'+ document['user'] +'_'+str(int(doc_timestamp))
		if not os.path.exists(user_dir):
			os.makedirs(user_dir)

		temp_folder_path = os.path.join(user_dir, "temp")
		if not os.path.exists(temp_folder_path):
			os.makedirs(temp_folder_path)

		temp_file_path = os.path.join(temp_folder_path, filename)
		with open(temp_file_path, 'w') as outfile:
			json.dump(document, outfile)
		final_file_path = os.path.join(user_dir, filename)
		shutil.copyfile(temp_file_path, final_file_path)
		os.remove(temp_file_path)

