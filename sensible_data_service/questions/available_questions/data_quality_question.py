from datetime import timedelta
import json
from multiprocessing import Pool
import time
import datetime
from collections import defaultdict
from calendar import monthrange

from db_access.named_queries.named_queries import NAMED_QUERIES
from sensible_audit import audit


# Name of the question
from utils.db_wrapper import DatabaseHelper

NAME = 'data_quality_question'

PROBES = {'bluetooth': {'database': 'edu_mit_media_funf_probe_builtin_BluetoothProbe', 'daily_expected_count': 288},
		  'calllog': {'database': 'edu_mit_media_funf_probe_builtin_CallLogProbe', 'daily_expected_count': 2},
			'sms': {'database': 'edu_mit_media_funf_probe_builtin_SMSProbe', 'daily_expected_count': 2},
			'wifi': {'database': 'edu_mit_media_funf_probe_builtin_WifiProbe', 'daily_expected_count': 144},
			'location': {'database': 'edu_mit_media_funf_probe_builtin_LocationProbe', 'daily_expected_count': 288}
}

db_helper = DatabaseHelper()
log = audit.getLogger(__name__)


def run():
	"""Main loop of data quality question. """
	print "Executing ", NAME
	print "Start time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	process_pool = Pool(5)
	process_pool.map(compute_data_quality_for_probe, PROBES.keys())
	print "End time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def compute_data_quality_for_probe(probe):
	users = [x['user'] for x in db_helper.execute_named_query(NAMED_QUERIES["get_unique_users_in_device_inventory"], None)]
	for user in users:
		timestamps = get_latest_timestamps_for_user_and_probe(user, probe)
		if not timestamps:
			continue
		daily_count = map_timestamps_to_days(timestamps)
		latest_scan_id = max(timestamps, key=lambda(timestamp): timestamp['id'])['id']
		rows = [(user, day.strftime('%Y-%m-%d %H:%M:%S'), daily_count[day],
				 probe, latest_scan_id) for day in daily_count]
		db_helper.execute_named_query(NAMED_QUERIES["update_qualities"], tuple(rows), readonly=False, bulk_insert=True)

def get_latest_timestamps_for_user_and_probe(user, probe):
	distinct_timestamps_query = NAMED_QUERIES["get_distinct_timestamps_by_user"]
	distinct_timestamps_query['database'] = PROBES[probe]['database']
	last_scan_ids = db_helper.retrieve({"limit": 10000, "fields": ['last_scan_id'], "users": [user], "where": {"type": [probe]}}, "data_quality")
	last_scan_id = 0
	if last_scan_ids:
		last_scan_id = max([scan_id.get("last_scan_id", 0) for scan_id in last_scan_ids])
	return db_helper.execute_named_query(distinct_timestamps_query, (user, last_scan_id)).fetchall()

def map_timestamps_to_days(timestamps):
	daily_count = defaultdict(int)
	for doc in timestamps:
		timestamp = doc['timestamp']
		daily_count[datetime.datetime(timestamp.year, timestamp.month, timestamp.day)] += 1
	return daily_count


def get_data_stats_for_period(request, user, scopes, users_to_return, user_roles, own_data):
	if "all" in users_to_return:
		users_to_return = [x['user'] for x in
				 db_helper.execute_named_query(NAMED_QUERIES["get_unique_users_in_device_inventory"], None)]
	print users_to_return
	start_date = request.REQUEST.get('start_date')
	end_date = request.REQUEST.get('end_date')
	data_type = request.REQUEST.get("data_type")

	params = []
	params += users_to_return
	params += [start_date]
	params += [end_date]
	params += [data_type]

	number_of_days = float((datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days)
	quality_named_query = NAMED_QUERIES["get_quality"]

	formatted_query = quality_named_query["query"] % (PROBES[data_type]["daily_expected_count"], number_of_days, ','.join(['%s'] * len(users_to_return)))
	month_stats = db_helper.execute_named_query({"database": quality_named_query["database"], "query": formatted_query}, tuple(params))
	return [{"user": doc["user"], "month_quality": float(doc["quality"]) if doc["quality"] else 0.0} for doc in month_stats.fetchall()]