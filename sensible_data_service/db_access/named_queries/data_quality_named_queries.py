users = ','.join(['%s'] * 814)
NAMED_QUERIES = {
        "get_distinct_timestamps_by_user": {
                "query": "select timestamp, max(id) as id from main where user = %s and id > %s  group by timestamp",
                "database" : 'edu_mit_media_funf_probe_builtin_BluetoothProbe'
        },

		"get_quality": {
			"query": "select user, sum(quality)/%s as quality from main where user in (%s) and timestamp between %%s and %%s and type = %%s group by user",
			"database": "data_quality"
		}

}