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