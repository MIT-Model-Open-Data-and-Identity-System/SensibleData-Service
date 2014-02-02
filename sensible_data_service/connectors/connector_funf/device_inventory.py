from utils import database
from collections import defaultdict
import json

class DeviceInventory(object):
	
	db = None

	def __init__(self):
		self.mapping = defaultdict(list)
		self.db = database.Database()
		for inventory in self.db.getDocuments(query={}, collection = 'device_inventory'):
			self.mapping[inventory['a_bt_mac']].append(inventory)


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

		
