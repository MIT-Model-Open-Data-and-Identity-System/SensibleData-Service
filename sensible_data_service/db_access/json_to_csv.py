import json
import sys
import hashlib
import base64
import time

def json_to_csv(json_obj, probe):
	probe = probe.replace('_researcher','').replace('_developer','')
	if 'facebook' in probe:
		return facebook_doc_to_csv(json_obj, probe)
	if 'funf' in probe:
		return funf_to_csv(json_obj, probe)
	if 'questionnaire' in probe:
		return questionnaire_to_csv(json_obj)
	raise ValueError(probe + ' is not a valid probe name')	
	

def facebook_birthday_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'birthday')


def facebook_education_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'education')


def facebook_feed_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'feed')


def facebook_friendrequests_to_csv(json_obj):
        fields = ['data', 'facebook_id', 'timestamp', 'user']
        return facebook_to_csv(json_obj, fields, 'friendrequests')

def facebook_friendlists_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'friendlists')


def facebook_friends_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'friends')


def facebook_groups_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'groups')


def facebook_hometown_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'hometown')


def facebook_interests_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'interests')


def facebook_likes_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'likes')


def facebook_location_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'location')


def facebook_locations_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'locations')


def facebook_political_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'political')


def facebook_religion_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'religion')


def facebook_statuses_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'statuses')


def facebook_work_to_csv(json_obj):
	fields = ['data', 'facebook_id', 'timestamp', 'user']
	return facebook_to_csv(json_obj, fields, 'work')

#Generic function for extracting fields for facebook without going into data
def facebook_to_csv(json_obj, fields, type):
	rows = []
	row = {}
	for v in json_obj:
		if not v in fields: continue
		if v == 'data':
			row[v] = base64.b64encode(json.dumps(json_obj[v]))
		else:
			row[v] = json_obj[v]

	row['data_type'] = type
	rows.append(row)
	return rows
	
def facebook_doc_to_csv(json_obj, collection):
	mtype = collection.split('_')[-1]
	if mtype == 'work': return facebook_work_to_csv(json_obj)
	if mtype == 'statuses': return facebook_statuses_to_csv(json_obj)
	if mtype == 'religion': return facebook_religion_to_csv(json_obj)
	if mtype == 'political': return facebook_political_to_csv(json_obj)
	if mtype == 'location': return facebook_location_to_csv(json_obj)
	if mtype == 'locations': return facebook_locations_to_csv(json_obj)
	if mtype == 'likes': return facebook_likes_to_csv(json_obj)
	if mtype == 'interests': return facebook_interests_to_csv(json_obj)
	if mtype == 'hometown': return facebook_hometown_to_csv(json_obj)
	if mtype == 'groups': return facebook_groups_to_csv(json_obj)
	if mtype == 'friendrequests': return facebook_friendrequests_to_csv(json_obj)
	if mtype == 'friends': return facebook_friends_to_csv(json_obj)
	if mtype == 'friendlists': return facebook_friendlists_to_csv(json_obj)
	if mtype == 'feed': return facebook_feed_to_csv(json_obj)
	if mtype == 'education': return facebook_education_to_csv(json_obj)
	if mtype == 'birthday': return facebook_birthday_to_csv(json_obj)
	raise ValueError(collection + ' is not a valid Facebook collection')

def funf_to_csv(json_obj, probe):
	if probe == 'edu_mit_media_funf_probe_builtin_BluetoothProbe': return funf_bluetooth_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_CallLogProbe': return funf_calllog_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_CellProbe': return funf_cell_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_ContactProbe': return funf_contact_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_HardwareInfoProbe': return funf_hardware_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_LocationProbe': return funf_location_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_ScreenProbe': return funf_screen_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_SMSProbe': return funf_sms_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_TimeOffsetProbe': return funf_timeoffset_to_csv(json_obj)
	if probe == 'edu_mit_media_funf_probe_builtin_WifiProbe': return funf_wifi_to_csv(json_obj)


def funf_metadata(json_obj):
	metadata = {}
	metadata['timestamp'] = json_obj['data']['TIMESTAMP']
	metadata['device_id'] = json_obj['device_id']
	metadata['sensible_token'] = json_obj['sensible_token']
	metadata['user'] = json_obj['user']
	metadata['uuid'] = json_obj['uuid']
	return metadata


def funf_bluetooth_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	for scan in json_obj['data']['DEVICES']:
		row = {}
		for key in metadata: row[key] = metadata[key]
		row['class'] = scan.get('android_bluetooth_device_extra_CLASS', dict()).get('mClass')
		row['bt_mac'] = scan.get('android_bluetooth_device_extra_DEVICE', dict()).get('mAddress')
		row['name'] = scan.get('android_bluetooth_device_extra_NAME')
		row['rssi'] = scan.get('android_bluetooth_device_extra_RSSI')
		rows.append(row)
	if len(json_obj['data']['DEVICES']) == 0:
		row = {}
		for key in metadata: row[key] = metadata[key]
		row['class'] = -1 
		row['bt_mac'] = '-1'
		row['name'] = '-1'
		row['rssi'] = 0
		rows.append(row)

	return rows


def funf_calllog_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['duration'] = json_obj['data'].get('duration')
	row['name'] = json_obj['data'].get('name')
	row['number'] = json_obj['data'].get('number')
	row['numbertype'] = json_obj['data'].get('numbertype')
	row['type'] = json_obj['data'].get('type')
	rows.append(row)

	return rows


def funf_cell_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['cid'] = json_obj['data'].get('cid', -1)
	row['lac'] = json_obj['data'].get('lac')
	row['psc'] = json_obj['data'].get('psc')
	row['type'] = json_obj['data'].get('type')
	rows.append(row)

	return rows


def funf_contact_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	for contact in json_obj['data']['CONTACT_DATA']:
		row = {}
		for key in metadata: row[key] = metadata[key]
		row['contact_id'] = json_obj['data'].get('contact_id')
		row['display_name'] = json_obj['data'].get('display_name')
		row['last_time_contacted'] = json_obj['data'].get('last_time_contacted')
		row['lookup'] = json_obj['data'].get('lookup')
		row['starred'] = json_obj['data'].get('starred')
		row['times_contacted'] = json_obj['data'].get('times_contacted')

		try: row['mimetype'] = contact['mimetype']
		except: row['mimetype'] = hashlib.md5(str(contact)).hexdigest()
		try: row['_id'] = contact['_id']
		except: pass
		try: row['data1'] = contact['data1']
		except: pass
		try: row['data2'] = contact['data2']
		except: pass
		try: row['data3'] = contact['data3']
		except: pass
		try: row['data4'] = contact['data4']
		except: pass
		try: rows.append(row)
		except: pass

	return rows


def funf_hardware_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['android_id'] = json_obj['data'].get('ANDROID_ID')
	row['bt_mac'] = json_obj['data'].get('BLUETOOTH_MAC')
	row['brand'] = json_obj['data'].get('BRAND')
	row['device_id'] = json_obj['data'].get('DEVICE_ID')
	row['model'] = json_obj['data'].get('MODEL')
	row['wifi_mac'] = json_obj['data'].get('WIFI_MAC')
	row['device'] = json_obj.get('device')
	row['device_bt_mac'] = json_obj.get('device_bt_mac')
	rows.append(row)

	return rows


def funf_location_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['lat'] = json_obj['data'].get('LOCATION', dict()).get('geojson', dict()).get('coordinates')[0]
	row['lon'] = json_obj['data'].get('LOCATION', dict()).get('geojson', dict()).get('coordinates')[1]
	row['accuracy'] = json_obj['data'].get('LOCATION', dict()).get('mAccuracy')
	row['provider'] = json_obj['data'].get('LOCATION', dict()).get('mProvider')
	rows.append(row)

	return rows


def funf_screen_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['screen_on'] = json_obj['data'].get('SCREEN_ON')
	rows.append(row)

	return rows


def funf_sms_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['address'] = json_obj['data'].get('address')
	row['body'] = json_obj['data'].get('body')
	row['person'] = json_obj['data'].get('person')
	row['protocol'] = json_obj['data'].get('protocol')
	row['message_read'] = json_obj['data'].get('read')
	row['service_center'] = json_obj['data'].get('service_center')
	row['status'] = json_obj['data'].get('status')
	row['subject'] = json_obj['data'].get('subject')
	row['thread_id'] = json_obj['data'].get('thread_id')
	row['type'] = json_obj['data'].get('type')
	rows.append(row)

	return rows


def funf_timeoffset_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	row = {}
	for key in metadata: row[key] = metadata[key]
	row['time_offset'] = json_obj['data'].get('TIME_OFFSET')
	rows.append(row)

	return rows


def funf_wifi_to_csv(json_obj):
	rows = []
	metadata = funf_metadata(json_obj)

	for scan in json_obj['data']['SCAN_RESULTS']:
		row = {}
		for key in metadata: row[key] = metadata[key]
		row['bssid'] = scan.get('BSSID')
		row['ssid'] = scan.get('SSID', "").encode('utf-8')
		row['level'] = scan.get('level')
		rows.append(row)
	if len(json_obj['data']['SCAN_RESULTS']) == 0:
		row = {}
		for key in metadata: row[key] = metadata[key]
		row['bssid'] = '-1' 
		row['ssid'] = '-1'
		row['level'] = 0
		rows.append(row)

	return rows


def questionnaire_to_csv(json_obj):
	rows = []
	row = {}
	row['form_version'] = json_obj.get('form_version')
	row['variable_name'] = json_obj.get('variable_name')
	if not json_obj['variable_name'].startswith("_"):
		row['human_readable_question'] = json_obj['human_readable_question'].encode('utf-8')
		row['human_readable_response'] = json_obj['human_readable_response'].encode('utf-8')

	row['timestamp'] = time.mktime(time.strptime(json_obj.get('last_answered')[:19],'%Y-%m-%d %H:%M:%S'))
	row['response'] = "".join([c for c in json_obj.get('response') if ord(c) < 128])
	row['user'] = json_obj.get('user')
	rows.append(row)

	return rows
