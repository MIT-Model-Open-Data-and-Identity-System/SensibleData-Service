<<<<<<< HEAD
=======
from db_access.named_queries import NAMED_QUERIES
from utils import db_wrapper
>>>>>>> devel
from collections import defaultdict
import MySQLdb

class DeviceInventory(object):

<<<<<<< HEAD
    db = None
=======
	def __init__(self):
		self.mapping = defaultdict(list)
		self.user_mapping = defaultdict(list)
		self.db = db_wrapper.DatabaseHelper()
		for inventory in self.db.execute_named_query(NAMED_QUERIES["get_device_inventory"], None):
			self.mapping[inventory['a_bt_mac']].append(inventory)
			self.user_mapping[inventory['user']].append(inventory)
>>>>>>> devel

    def __init__(self):
        self.mapping = defaultdict(list)
        #self.db = db_wrapper.DatabaseHelper()
        connection = MySQLdb.connect("ec2-54-229-83-210.eu-west-1.compute.amazonaws.com", "magda", "Change.me", "common_admin")
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from device_inventory")
        #for inventory in self.db.execute_named_query(NAMED_QUERIES["get_device_inventory"], None):
        for inventory in cursor:
            self.mapping[inventory['a_bt_mac']].append(inventory)

<<<<<<< HEAD
=======
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
>>>>>>> devel

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
