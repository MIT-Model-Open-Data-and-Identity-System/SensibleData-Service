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
	},

  "question_lasse_bluetooth_network": {
        "query": """insert into question_lasse_bluetooth_network.main (user_from, user_to, timestamp, latest_timestamp)
            (select 
                main.user as user_from, 
                device_inventory.user as user_to, 
                date(timestamp) as timestamp,
                edu_mit_media_funf_probe_builtin_BluetoothProbe.main.timestamp as latest_timestamp
            from edu_mit_media_funf_probe_builtin_BluetoothProbe.main join common_admin.device_inventory on device_inventory.bt_mac = main.bt_mac
            where 
                main.bt_mac != '-1' and (
                    hour(edu_mit_media_funf_probe_builtin_BluetoothProbe.main.timestamp) < %s or 
                    hour(edu_mit_media_funf_probe_builtin_BluetoothProbe.main.timestamp) >= %s
                ) and
                edu_mit_media_funf_probe_builtin_BluetoothProbe.main.timestamp > %s
      )
            on duplicate key update 
                occurrences = occurrences+1,
                latest_timestamp = edu_mit_media_funf_probe_builtin_BluetoothProbe.main.timestamp""",
        "database": "question_lasse_bluetooth_network",
        "write": True
    },

  "question_lasse_bluetooth_network_delete_dates": {
      "query": """delete from main
                  where timestamp between %s and %s""",
      "database": "question_lasse_bluetooth_network",
      "write": True
  },



}