import json
from django.conf import settings
import os
import time
import shutil


class FileSystemWrapper:
	def insert(self, documents, probe, role):
		for document in documents:
			self.store_document_on_file_server(document, probe, role)

	def store_document_on_file_server(self, document, probe, role=None):
		if role is None:
			role = "main"
		user_dir = os.path.join(settings.FILESYSTEM_DATABASE["LOCAL_DIR"], probe, role, document['user'])
		try:
			filename = document['_id']
		except KeyError:
			return
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

wrapper = FileSystemWrapper()

if __name__ == "__main__":
	for filename in os.listdir("tests/test_data/"):
		filename = filename.replace(".json", "").replace("_test", "")
		# try:
		wrapper.insert([json.loads(line) for line in open("tests/test_data/" + filename + ".json", "r")], filename, None)
		# except BaseException, e:
		#
		# 	print str(e)