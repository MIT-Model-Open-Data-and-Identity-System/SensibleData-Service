DATABASE = {
			"backend":"mongodb",
			"params":
				{
					"url":"mongodb://%s:%s@ds045047.mongolab.com:45047/sensibledtu-data",
					"database":"sensibledtu-data"
				}
		}

AUTH_DATABASE = {
			"backend":"mongodb",
			"params":
				{
					"url":"mongodb://%s:%s@ds035237.mongolab.com:35237/sensibledtu-auth",
					"database":"sensibledtu-auth"
				}
		}


FUNF = {
	"upload_path" : "/sensible-data/connector_funf/upload/", #must be www-data writable
	"upload_not_authorized_path" : "/sensible-data/connector_funf/upload_not_authorized/", #must be www-data writable


	}


LOG_FILE_PATH = "/sensible-data/log/" #must be www-data writable
