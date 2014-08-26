from collections import defaultdict

from db_access.named_queries.named_queries import NAMED_QUERIES
from utils import db_wrapper


class DeviceInventory(object):
	
	db = None

	def __init__(self):
		self.mapping = defaultdict(list)
		self.user_mapping = defaultdict(list)
		self.db = db_wrapper.DatabaseHelper()
		for inventory in self.db.execute_named_query(NAMED_QUERIES["get_device_inventory"], None):
			self.mapping[inventory['a_bt_mac']].append(inventory)
			self.user_mapping[inventory['user']].append(inventory)


	def map_user_to_bluetooth_mac(self, user, timestamp):
		devices = self.user_mapping[user]
		for device in devices:
			if device['start'] <= timestamp and device['end'] > timestamp:
				return device['a_bt_mac']
		return None

	def mapBtToUser(self, bt_mac, timestamp, use_mac_if_empty=True):
		devices = self.mapping[bt_mac]
		if len(devices) == 0: 
			if use_mac_if_empty: return bt_mac
			else: return None
		if len(devices) == 1: return devices[0]['user']

		for d in devices:
			if d['start'] <= timestamp and d['end'] > timestamp:
				return d['user']

		if use_mac_if_empty: return bt_mac
		else: return None

		
