import os, sys
try:
        lib_path = os.path.abspath('../../utils')
        sys.path.append(lib_path)
        from auth_database import AuthDatabase
        import service_config
        import SECURE_service_config
except ImportError:
        from utils.auth_database import AuthDatabase
        from utils import service_config
        from utils import SECURE_service_config

class ConnectorPipe(object):
	auth_db = None
	
	def __init__(self):
		self.auth_db = AuthDatabase()

	def isAuthorized(self):
		pass
		
