import json
import time
from db_access.named_queries.named_queries import NAMED_QUERIES
from django.contrib.auth.models import User

NAME = "aggregate_questionnaire_question"

from utils import db_wrapper

db_helper = db_wrapper.DatabaseHelper()

def get_aggregated_questionnaire_data(request, user, scopes, users_to_return, user_roles, own_data):
	form_version = request.REQUEST.get("form_version", "")
	if not form_version:
		return {"status": {"code": 400, "message": "Please select a questionnaire version"}}
	if "all" in users_to_return:
		users = User.objects.all()
                users_to_return = [user.username for user in users if not hasattr(user, "userrole")]
	response = []
	all_variable_names = ['user', 'timestamp']
	all_variable_names.extend([doc['variable_name'] for doc in
				   db_helper.execute_named_query(NAMED_QUERIES["get_variable_names"], (form_version)).fetchall()])

	for user in users_to_return:
		results = {}
		timestamp = -1
		results["user"] = '"' + user + '"'
		for result in db_helper.retrieve({"limit": 10000, "users": [user], "fields": ["variable_name", "response", "timestamp"],
										  "where": {"form_version": [form_version]}},
										 "dk_dtu_compute_questionnaire").fetchall():
			results[result['variable_name']] = '"' + result['response'].replace('"', '').replace("\n", " ").replace("\r", " ") + '"'
			if result['variable_name'] == '_submitted' and result['response'] == "true":
				timestamp = int(time.mktime(result['timestamp'].timetuple()))
		results["timestamp"] = '"' + str(timestamp) + '"'

		missing_variable_names = missing_variable_names =  set(all_variable_names) - set(results.keys())
		for variable_name in missing_variable_names:
			results[variable_name] = ""
		response.append(results)

	return {"results": response, "meta": {}}

