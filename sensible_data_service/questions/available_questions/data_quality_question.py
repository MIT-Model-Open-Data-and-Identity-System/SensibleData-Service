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

PROBES = {#'edu_mit_media_funf_probe_builtin_BluetoothProbe': {'tag': 'bluetooth', 'daily_expected_count': 288},
		  'edu_mit_media_funf_probe_builtin_CallLogProbe': {'tag': 'calllog', 'daily_expected_count': 2},
			'edu_mit_media_funf_probe_builtin_SMSProbe': {'tag': 'sms', 'daily_expected_count': 2},
	#		'edu_mit_media_funf_probe_builtin_WifiProbe': {'tag': 'wifi', 'daily_expected_count': 144},
	#		'edu_mit_media_funf_probe_builtin_LocationProbe': {'tag': 'location', 'daily_expected_count': 288}
}

# Quality settings
MONTH_EXP = 8640.0
WEEK_EXP = 2016.0
HOUR_EXP = 12.0
DAY_EXP = 288.0
MAX_GRADE = 1.0

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
		rows = [{"user": user, "timestamp": day.strftime('%Y-%m-%d %H:%M:%S'), "count": daily_count[day],
				 "type": PROBES[probe]['tag'], "last_scan_id": latest_scan_id, "quality": min(1.0, daily_count[day]/PROBES[probe]['daily_expected_count'])} for day in daily_count]
		db_helper.insert_rows(rows, "data_quality")

def get_latest_timestamps_for_user_and_probe(user, probe):
	distinct_timestamps_query = NAMED_QUERIES["get_distinct_timestamps_by_user"]
	distinct_timestamps_query['database'] = probe
	last_scan_id_result = db_helper.retrieve({"limit": 1, "fields": ['last_scan_id'], "users": [user], "where": {"type": [PROBES[probe]['tag']]}}, "data_quality").fetchone()
	last_scan_id = 0
	if last_scan_id_result:
		last_scan_id = last_scan_id_result.get("last_scan_id", 0)
	return db_helper.execute_named_query(distinct_timestamps_query, (user, last_scan_id)).fetchall()

def map_timestamps_to_days(timestamps):
	daily_count = defaultdict(int)
	for doc in timestamps:
		timestamp = doc['timestamp']
		daily_count[datetime.datetime(timestamp.year, timestamp.month, timestamp.day)] += 1
	return daily_count


def get_data_stats_for_period(request, users, data_type, output_type, start_date, end_date):
	if users == "all":
		users = [x['user'] for x in
				 db_helper.execute_named_query(NAMED_QUERIES["get_unique_users_in_device_inventory"], None)]

	print len(users)
	params = []
	params += users
	params += [start_date]
	params += [end_date]
	params += [data_type]

	number_of_days = float((datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')).days)
	quality_named_query = NAMED_QUERIES["get_quality"]

	formatted_query = quality_named_query["query"] % (number_of_days, ','.join(['%s'] * len(users)))
	month_stats = db_helper.execute_named_query({"database": quality_named_query["database"], "query": formatted_query}, tuple(params))
	return json.dumps([{"user": doc["user"], "month_quality": doc["quality"] if doc["quality"] else 0.0} for doc in month_stats.fetchall()])