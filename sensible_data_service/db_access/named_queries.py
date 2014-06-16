NAMED_QUERIES = {
	"select_questionnaires" :{
		"query": "select user, variable_name, response from main",
		"database": "dk_dtu_compute_questionnaire"
	},

	"count_unique_facebook_users": {
		"query": "select count(distinct user) from main where data_type = %s",
		"database": "dk_dtu_compute_facebook"
	},

	"count_unique_questionnaire_users": {
		"query": "select count(distinct user) from main",
		"database": "dk_dtu_compute_questionnaire"
	},

	"count_questionnaire_users_with_variable": {
		"query": "select count(*) from main where variable_name = %s",
		"database": "dk_dtu_compute_questionnaire"
	},

	"count_questionnaire_users_by_sex": {
		"query": "select count(*) from main where variable_name = 'sex' and response = %s",
		"database": "dk_dtu_compute_questionnaire"
	},

	"count_funf_unique_users_by_probe": {
		"query": "select count(distinct user) from main",
		#default probe database.
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
	},

        ### get_unique_users_locationprobe

        "get_unique_users_locationprobe_developer": {
		"query": "select distinct user from developer",
		"database": "edu_mit_media_funf_probe_builtin_LocationProbe"
	},

        "get_unique_users_locationprobe_researcher": {
		"query": "select distinct user from researcher",
		"database": "edu_mit_media_funf_probe_builtin_LocationProbe"
	},

        "get_unique_users_locationprobe_main": {
		"query": "select distinct user from main",
		"database": "edu_mit_media_funf_probe_builtin_LocationProbe"
	},

        ### delete_stops

        "delete_stops_developer": {
                "query": "delete from developer where user = %s",
		"database": "question_stop_locations"
        },

        "delete_stops_researcher": {
                "query": "delete from researcher where user = %s",
		"database": "question_stop_locations"
        },

        "delete_stops_main": {
                "query": "delete from main where user = %s",
		"database": "question_stop_locations"
        },

        ### delete_resampled_location

        "delete_resampled_location_developer": {
                "query": "delete from developer where (timestamp between %s and %s)",
		"database": "resampled_location"
        },

        "delete_resampled_location_researcher": {
                "query": "delete from researcher where (timestamp between %s and %s)",
		"database": "resampled_location"
        },

        "delete_resampled_location_main": {
                "query": "delete from main where (timestamp between %s and %s)",
		"database": "resampled_location"
        },

	"get_unique_users_in_device_inventory": {
		"query": "select distinct user from device_inventory",
		"database": "common_admin"
	},

	"get_device_inventory": {
		"query": "select * from device_inventory",
		"database": "common_admin"
	},

	"get_device_inventory_with_device_id": {
		"query": "select * from device_inventory where device_id = %s order by timestamp desc",
		"database": "common_admin"
	}
}