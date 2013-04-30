import os, sys
try:
	lib_path = os.path.abspath('../../utils')
	sys.path.append(lib_path)
	from database import Database
	import service_config
	import SECURE_service_config
except ImportError:
	from utils.database import Database
	from utils import service_config
	from utils import SECURE_service_config

class Connector(object):
	db = None

	def __init__(self):
		self.db = Database()


