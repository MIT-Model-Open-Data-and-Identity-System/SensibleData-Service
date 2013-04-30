from connector_pipes.connector_pipe import connector_pipe

class ConnectorFunfPipe(connector_pipe.ConnectorPipe):
	def __init__(self):
		super(ConnectorFunfPipe, self).__init__()
		pass


	def getUser(self, token):
		return ""
