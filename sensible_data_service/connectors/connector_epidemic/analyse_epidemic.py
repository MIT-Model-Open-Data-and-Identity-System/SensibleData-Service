from sensible_audit import audit
from utils import db_wrapper
import base64
import json
import datetime
from collections import defaultdict
from connectors.connector_funf import device_inventory

log = audit.getLogger(__name__)

USER = '757b0530d13b3de4916324199ded90'

def analyse_epidemic():
	db = db_wrapper.DatabaseHelper()
	#cur = db.retrieve(params={'limit':1000, 'sortby':'timestamp', 'order':-1, 'where': {'user':[USER]}}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
	cur = db.retrieve(params={'limit':10000000, 'sortby':'timestamp', 'order':-1, 'start_date': 1407794400, 'end_date': 1407880800}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
	lt = 0
	
	inventory = device_inventory.DeviceInventory()

	states = defaultdict(set)

	for row in cur:
		data = json.loads(base64.b64decode(row['data']))
		user = row['user']
		timestamp = row['timestamp']
		timestamp_2 = data['TIMESTAMP']
	#	if not (timestamp_2 >= 1407708000 and timestamp_2 <= 1407794400): continue



#		print user, timestamp, timestamp_2, lt - timestamp_2, data['self_state'], data['infected_tag'], data['to_recover_time'],
	#	try: print data['self_state'], timestamp
	#	except: print ''
	#	except: pass
		
		states[user].add(data['self_state'])
		lt = timestamp_2
		#if timestamp < datetime.datetime(2014, 07, 29): continue



	final_states = defaultdict(str)

	for user in states:
		if 'I' in states[user]: final_states[user] = 'I'
		elif 'E' in states[user]: final_states[user] = 'I'
		elif 'V' in states[user]: final_states[user] = 'V'
		elif 'S' in states[user]: final_states[user] = 'S'



	global_states = defaultdict(int)

	for user in final_states:
		global_states[final_states[user]] += 1

	print global_states
	
	cur = db.retrieve(params={'limit':10000000, 'sortby':'timestamp', 'order':-1, 'start_date': 1407794400, 'end_date': 1407880800, 'where': {'user': [USER]}}, collection='edu_mit_media_funf_probe_builtin_BluetoothProbe', roles='')

	interactions = set()

	for row in cur:
		if row['timestamp_added'] < row['timestamp'] : continue
		user = row['user']
		timestamp = row['timestamp']
		bt_mac = row['bt_mac']
		if bt_mac == '-1': continue
		userB = inventory.mapBtToUser(bt_mac, long(timestamp.strftime('%s')))
		if userB == bt_mac: continue
	
		interactions.add(userB)


	for user in interactions:
		print user, final_states[user]
