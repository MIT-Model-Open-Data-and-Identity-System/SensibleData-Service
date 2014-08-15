NAMED_QUERIES = {
        "get_distinct_timestamps_by_user": {
                "query": "select timestamp, max(id) as id from main where user = %s and id > %s  group by timestamp",
                "database" : 'edu_mit_media_funf_probe_builtin_BluetoothProbe'
        }
}