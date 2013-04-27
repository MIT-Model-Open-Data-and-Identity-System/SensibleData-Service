import json

class Config:

	CONFIG_LOCATION = '/home/arks/MODIS/Sensible-Data-Service/sensible_data_service/project_config'
	SECURE_CONFIG_LOCATION = '/home/arks/MODIS/Sensible-Data-Service/sensible_data_service/secure_project_config'
	config = None
	secure_config = None

	def __init__(self):
		self.config = json.loads(open(self.CONFIG_LOCATION).read())
		self.secure_config = json.loads(open(self.SECURE_CONFIG_LOCATION).read())

