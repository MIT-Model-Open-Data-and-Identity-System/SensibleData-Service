from connector_pipes.connector_pipe import connector_pipe

class ConnectorFunfPipe(connector_pipe.ConnectorPipe):
	def __init__(self):
		super(ConnectorFunfPipe, self).__init__()


	def getAuthorization(self, token, scope):
		return self.authorizationManager.getAuthorizationForToken('connector_funf', scope, token)
