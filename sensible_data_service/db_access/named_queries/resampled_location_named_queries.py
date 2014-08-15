NAMED_QUERIES = {
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
        }
}
