NAMED_QUERIES = {
        "get_distinct_timestamps_by_user": {
                "query": "select timestamp, max(id) as id from %s where user = %%s and id > %%s  group by timestamp",
                "database" : 'edu_mit_media_funf_probe_builtin_BluetoothProbe'
        },

		"get_quality": {
			"query": "select user, sum(least(1.0, count/%s))/%s as quality from %s where user in (%s) and timestamp between %%s and %%s and type = %%s group by user",
			"database": "data_quality"
		},

		"update_qualities": {
			"query": "insert into %s (user, timestamp, count, type, last_scan_id) values (%%s, %%s, %%s, %%s, %%s) on duplicate key update count = count + values(count), last_scan_id = values(last_scan_id)",
			"database": "data_quality"
		}

}