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
	},
 
 	## who_did_i_see_question
 
     #select
     "get_last_scan_id_main": {
		"query": "SELECT MAX(scan_id) FROM main;",
		"database": "question_who_did_i_see"
	},
 
      "get_last_scan_id_developer": {
		"query": "SELECT MAX(scan_id) FROM developer;",
		"database": "question_who_did_i_see"
	},
 
      "get_last_scan_id_researcher": {
		"query": "SELECT MAX(scan_id) FROM researcher;",
		"database": "question_who_did_i_see"
	},
 
     #####
     "get_new_scan_chunk_main": {
		"query": "SELECT id, user, bt_mac, timestamp FROM main WHERE id > %s AND id < %s ORDER BY timestamp",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      "get_new_scan_chunk_developer": {
		"query": "SELECT id, user, bt_mac, timestamp FROM developer WHERE id > %s AND id < %s ORDER BY timestamp",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      "get_new_scan_chunk_researcher": {
		"query": "SELECT id, user, bt_mac, timestamp FROM researcher WHERE id > %s AND id < %s ORDER BY timestamp",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      #####
      "get_distinct_users_from_main": {
		"query": "SELECT distinct user FROM main",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      "get_distinct_users_from_researcher": {
		"query": "SELECT distinct user FROM researcher",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      "get_distinct_users_from_developer": {
		"query": "SELECT distinct user FROM developer",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      #####
      "get_user_seen_in_time_main": {
		"query": "SELECT user_seen, time, timestamp FROM main WHERE user = %s AND (timestamp BETWEEN %s AND %s)",
		"database": "question_who_did_i_see"
      }, 
      
      "get_user_seen_in_time_developer": {
		"query": "SELECT user_seen, time, timestamp FROM developer WHERE user = %s AND (timestamp BETWEEN %s AND %s)",
		"database": "question_who_did_i_see"
      },
      
      "get_user_seen_in_time_researcher": {
		"query": "SELECT user_seen, time, timestamp FROM researcher WHERE user = %s AND (timestamp BETWEEN %s AND %s)",
		"database": "question_who_did_i_see"
      },
      
      #####
      "get_bt_mac_seen_main": {
		"query": "SELECT bt_mac FROM main WHERE user = %s AND (timestamp BETWEEN %s AND %s)",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },   
      
      "get_bt_mac_seen_developer": {
		"query": "SELECT bt_mac FROM developer WHERE user = %s AND (timestamp BETWEEN %s AND %s)",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      "get_bt_mac_seen_researcher": {
		"query": "SELECT bt_mac FROM researcher WHERE user = %s AND (timestamp BETWEEN %s AND %s)",
		"database": "edu_mit_media_funf_probe_builtin_BluetoothProbe"
      },
      
      #insert
      "insert_who_did_i_see_main": {
		"query": "INSERT INTO main (user, user_seen, timestamp, time, scan_id) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time = time + %s",
		"database": "question_who_did_i_see"        
      },
      
      "insert_who_did_i_see_developer": {
		"query": "INSERT INTO developer (user, user_seen, timestamp, time, scan_id) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time = time + %s",
		"database": "question_who_did_i_see"        
      },
      
      "insert_who_did_i_see_researcher": {
		"query": "INSERT INTO researcher (user, user_seen, timestamp, time,scan_id) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE time = time + %s",
		"database": "question_who_did_i_see"        
      }
 }