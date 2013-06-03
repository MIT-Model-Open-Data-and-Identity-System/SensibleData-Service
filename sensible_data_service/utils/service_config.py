BASE_PATH = "/home/arks/MODIS/Sensible-Data-Service/sensible_data_service"
DATA_BASE_PATH = ""

DATABASE = {
			"backend":"mongodb",
			"params": {
					"url":"mongodb://%s:%s@ds059557.mongolab.com:59557/sensible-data2",
					"database":"sensible-data2"
			}
}

AUTH_DATABASE = {
			"backend":"mongodb",
			"params": {
					"url":"mongodb://%s:%s@ds035237.mongolab.com:35237/sensibledtu-auth",
					"database":"sensibledtu-auth"
			}
}


LOG_FILE_PATH = DATA_BASE_PATH+"/sensible-data/log/" #must be www-data writable
SERVICE_NAME = "SensibleDTU-1k"

PLATFORM = {
	"platform_uri": "http://166.78.249.214:8081/",
	"platform_uri_token": "http://166.78.249.214:8081/oauth2/oauth2/token/",
	"platform_uri_dashboard": "http://166.78.249.214:8081/dashboard/",
	"redirect_uri": "http://166.78.249.214:8082/platform_api/redirect_uri/",
	"required_scopes": ["enroll", "view_real_name"],
	"ip_addr": ["166.78.249.214", "18.111.3.213"]
}

CONNECTORS = {
	"ConnectorFunf": True,
	"ConnectorFacebook": False,

}
