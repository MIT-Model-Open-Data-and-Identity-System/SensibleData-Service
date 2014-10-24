from django.contrib.auth.models import User
from django.db.models import Max
import time
from accounts.models import UserRole
from connectors.connector_funf.device_inventory import DeviceInventory
from db_access.named_queries.named_queries import NAMED_QUERIES
from questions.models import SensibleBluetoothScan
from utils import db_wrapper
import pytz

NAME = "bluetooth_network_question"

db_helper = db_wrapper.DatabaseHelper()
device_inventory = DeviceInventory()


def run():
	users = get_users_for_role("main")
	print users
	for user in users:
		save_sensible_connections_for_user(user)


def save_sensible_connections_for_user(user):
	bt_scans = get_bluetooth_scans_for_user(user)
	if len(bt_scans) == 0: return
	max_scan_id = max(bt_scans, key=lambda(bt_scan): bt_scan['id'])['id']
	sensible_scans = []
	for scan in bt_scans:
		scanned_user = device_inventory.mapBtToUser(scan['bt_mac'], int(time.mktime(scan['timestamp'].timetuple())), use_mac_if_empty=False)
		if not scanned_user:
			continue

		sensible_scans.append(SensibleBluetoothScan(timestamp=pytz.timezone("Europe/Copenhagen").localize(scan['timestamp']), scanning_user=scan['user'], scanned_user=scanned_user, rssi=scan['rssi'], last_scan_id=max_scan_id))
	SensibleBluetoothScan.objects.bulk_create(sensible_scans)


def get_users_for_role(role):
	users = User.objects.all()
	if role == "main":  # return all users without a role (students)
		return [user.username for user in users if not hasattr(user, "userrole")]
	users_with_roles = [user for user in users if hasattr(user, "userrole")]
	user_roles = UserRole.objects.filter(user__in=users_with_roles)

	return [user_role.user.username for user_role in user_roles if role in user_role.roles.values_list("role", flat=True)]


def get_bluetooth_scans_for_user(user, role="main"):
	distinct_timestamps_query = NAMED_QUERIES["get_bt_scans_by_user"]
	formatted_query = distinct_timestamps_query["query"] % role
	distinct_timestamps_query['database'] = "edu_mit_media_funf_probe_builtin_BluetoothProbe"

	last_scan_id = SensibleBluetoothScan.objects.all().aggregate(Max('last_scan_id'))["last_scan_id__max"]
	if not last_scan_id:
		last_scan_id = 0
	return db_helper.execute_named_query({"query": formatted_query, "database": "edu_mit_media_funf_probe_builtin_BluetoothProbe" }, (user, last_scan_id)).fetchall()

