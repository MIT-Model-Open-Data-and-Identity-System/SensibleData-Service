import json
from db_access.named_queries.named_queries import NAMED_QUERIES

NAME = "aggregate_questionnaire_question"

from utils import db_wrapper

db_helper = db_wrapper.DatabaseHelper()

def get_aggregated_questionnaire_data(request, user, scopes, users_to_return, user_roles, own_data):
	form_version = request.REQUEST.get("form_version", "")
	if not form_version:
		return {"status": {"code": 400, "message": "Please select a questionnaire version"}}
	if "all" in users_to_return:
		users_to_return = [x['user'] for x in
						   db_helper.execute_named_query(NAMED_QUERIES["get_unique_users_in_device_inventory"], None)]
	response = []
	header = ['user']
	header.extend([doc['variable_name'] for doc in
				   db_helper.execute_named_query(NAMED_QUERIES["get_variable_names"], (form_version)).fetchall()])
	response.append(",".join(header))
	for user in users_to_return:
		results = {}
		for result in db_helper.retrieve({"limit": 10000, "users": [user], "fields": ["variable_name", "response"],
										  "where": {"form_version": [form_version]}},
										 "dk_dtu_compute_questionnaire").fetchall():
			results[result['variable_name']] = '"' + result['response'].replace('"', '').replace("\n", " ").replace(
				"\r", " ") + '"'
		line = ['"' + user + '"']
		line.extend([results.get(variable_name, "") for variable_name in header if variable_name != 'user'])
		response.append(",".join(line))
	return "#" + json.dumps({"status": {"code": 200, "message": "OK", "length": str(len(response))}}) + "\n" + "\n".join(response)