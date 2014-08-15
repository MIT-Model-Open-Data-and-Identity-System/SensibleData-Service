NAMED_QUERIES = {


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
	}

}