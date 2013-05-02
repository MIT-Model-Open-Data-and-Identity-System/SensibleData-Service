DATABASE = {
			"backend":"mongodb",
			"params": {
					"url":"mongodb://%s:%s@ds045047.mongolab.com:45047/sensibledtu-data",
					"database":"sensibledtu-data"
			}
}

AUTH_DATABASE = {
			"backend":"mongodb",
			"params": {
					"url":"mongodb://%s:%s@ds035237.mongolab.com:35237/sensibledtu-auth",
					"database":"sensibledtu-auth"
			}
}


LOG_FILE_PATH = "/sensible-data/log/" #must be www-data writable
SERVICE_NAME = "SensibleDTU-1k" #must be www-data writable


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
			"upload_path": "/sensible-data/connector_funf/upload/", #must be www-data writable
			"upload_not_authorized_path" : "/sensible-data/connector_funf/upload_not_authorized/", #must be www-data writable
			"decrypted_path" : "/sensible-data/connector_funf/decrypted/", #must be www-data writable
			"decryption_failed_path" : "/sensible-data/connector_funf/decryption_failed/", #must be www-data writable
			"load_failed_path" : "/sensible-data/connector_funf/load_failed/", #must be www-data writable
			"config_path": "/sensible-data/connector_funf/config/", #must be www-data writable
			"backup_path": "/sensible-data/connector_funf/backup/", #must be www-data writable
			"connector_type": "resource_provider", #client registers to this connector
			"max_population_processes": 4,
			"max_population_files": 10,

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
			"connector_type": "client"

		}
	}


}
