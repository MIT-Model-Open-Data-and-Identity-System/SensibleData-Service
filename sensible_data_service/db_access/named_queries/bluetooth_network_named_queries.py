NAMED_QUERIES = {
        "get_bt_scans_by_user": {
                "query": "select timestamp, user, bt_mac, rssi max(id) as id from %s where user = %%s and id > %%s  group by timestamp",
                "database" : 'edu_mit_media_funf_probe_builtin_BluetoothProbe'
        },

}
