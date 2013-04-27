import os, sys
lib_path = os.path.abspath('../../utils')
sys.path.append(lib_path)
from database import Database


class Connector:
	db = None
	
	def __init__(self):
		db = Database()
		db.insertDocument({'hello':'world'}, 'test')


connector = Connector()
