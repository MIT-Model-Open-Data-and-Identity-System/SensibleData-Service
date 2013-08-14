from django.conf import settings

#TODO: separate paths for 'processing'

DATA_BASE_DIR = settings.DATA_BASE_DIR

CONNECTORS = {
	"ConnectorFunf": {
		"name": "connector_funf",
		"description": "This software runs on your phone and collects data.",
		"scopes": {
			"all_probes": {
				"description": "This scope grants access to all the data collected by Funf on your phone.",
			}

		},
		"config": {
			"upload_path": DATA_BASE_DIR + "/sensible-data/connector_funf/upload/", #must be www-data writable
			"upload_not_authorized_path" : DATA_BASE_DIR + "/sensible-data/connector_funf/upload_not_authorized/", #must be www-data writable
			"decrypted_path" : DATA_BASE_DIR + "/sensible-data/connector_funf/decrypted/", #must be www-data writable
			"decryption_failed_path" : DATA_BASE_DIR + "/sensible-data/connector_funf/decryption_failed/", #must be www-data writable
			"load_failed_path" : DATA_BASE_DIR + "/sensible-data/connector_funf/load_failed/", #must be www-data writable
			"decrypted_not_authorized" : DATA_BASE_DIR + "/sensible-data/connector_funf/decrypted_not_authorized/",
			"config_path": DATA_BASE_DIR + "/sensible-data/connector_funf/config/config.json", #must be www-data writable
			"backup_path": DATA_BASE_DIR + "/sensible-data/connector_funf/backup/", #must be www-data writable
			"connector_type": "client",
			"max_population_processes": 4,
			"max_population_files": 100,
			"grant_url" : "http://test.com",
			"revoke_url": "http://test.com",

			},
		"schedule": {

			}

		},
	"ConnectorQuestionnaire": {
		"name": "connector_questionnaire",
		"description": "This is a questionnaire application.",
		"scopes": {
			"input_form_data": {
				"description": "This scope allows the application to submit your data.",
				}

			},
		"config": {
			"connector_type": "client",
			"grant_url" : "http://test.com",
			"revoke_url": "http://test.com",

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
