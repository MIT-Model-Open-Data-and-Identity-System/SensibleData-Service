import os, sys
try:
        lib_path = os.path.abspath('../../utils')
        sys.path.append(lib_path)
        import service_config
        import SECURE_service_config
except ImportError:
        from utils.auth_database import AuthDatabase
        from utils import service_config
        from utils import SECURE_service_config
	#from authorization_manager.authorization_manager import AuthorizationManager

class ConnectorPipe(object):
	#authorizationManager = None
	
	def __init__(self):
	#	self.authorizationManager = AuthorizationManager()
		pass

