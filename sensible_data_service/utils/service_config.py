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


#TODO: separate paths for 'processing'
CONNECTORS = {
	"connector_funf": {
		"scopes": {
			"all_probes": {
				"grant_url" : "",
				"revoke_url": "",
				"description": "This scope grants access to all the data collected by Funf on your phone."
			}

		},
		"config": {
			"upload_path": DATA_BASE_PATH+"/sensible-data/connector_funf/upload/", #must be www-data writable
			"upload_not_authorized_path" : DATA_BASE_PATH+"/sensible-data/connector_funf/upload_not_authorized/", #must be www-data writable
			"decrypted_path" : DATA_BASE_PATH+"/sensible-data/connector_funf/decrypted/", #must be www-data writable
			"decryption_failed_path" : DATA_BASE_PATH+"/sensible-data/connector_funf/decryption_failed/", #must be www-data writable
			"load_failed_path" : DATA_BASE_PATH+"/sensible-data/connector_funf/load_failed/", #must be www-data writable
			"config_path": DATA_BASE_PATH+"/sensible-data/connector_funf/config/", #must be www-data writable
			"backup_path": DATA_BASE_PATH+"/sensible-data/connector_funf/backup/", #must be www-data writable
			"connector_type": "client",
			"max_population_processes": 4,
			"max_population_files": 100,

		},
		"schedule": {

		}

	},
	"connector_facebook": {
		"scopes": {
			"read_friendlists": {
				"descritpion": "Provides access to any friend lists the user created. All user's friends are provided as part of basic data, this extended permission grants access to the lists of friends a user has created, and should only be requested if your application utilizes lists of friends."
				
			}

		},
		"config": {
			"connector_type": "resource"

		}
	}


}
