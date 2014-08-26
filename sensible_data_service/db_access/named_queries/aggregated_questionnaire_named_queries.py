NAMED_QUERIES = {
	"get_variable_names": {
		"query": "select distinct variable_name from main where form_version=%s",
		"database": "dk_dtu_compute_questionnaire"
	}
}