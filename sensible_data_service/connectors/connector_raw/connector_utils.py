from collections import OrderedDict

class BadRequestException(Exception):
	def __init__(self, value):
		self.value = value

	def __init__(self, status, code, description):
		self.value = {}
		self.value['status'] = status
		self.value['code'] = code
		self.value['desc'] = description

	def __str__(self):
		return repr(self.value)

def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	if string == 'true': return True
	return False

def array_to_csv(array, collection):
	output = ''
	if 'bluetooth' in collection.lower():
		return bluetooth_to_csv(array, output)	
	elif 'location' in collection.lower():
		return location_to_csv(array, output)
	elif 'wifi' in collection.lower():
		return wifi_to_csv(array, output)
	elif 'sms' in collection.lower():
		return sms_to_csv(array, output)
	elif 'calllog' in collection.lower():
		return calllog_to_csv(array, output)
	elif 'likes' in collection.lower():
		return likes_to_csv(array,output)
	else:
		return 'We do not yet support csv output for ' + collection + ' data. Sorry!'

def likes_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','data.category','facebook_id']
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n' 
	output_lines = [] 
	for row in array:
		try:
			if len(row['data']) > 0:
				for result in row['data']:
					temp = '"' + row['user'] + '",' + str(row['timestamp']) + ',' 
					try:
						temp += '"' + str(result['id']) + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + result['category'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def wifi_to_csv(array, output):
	fields = ['user','data.TIMESTAMP','BSSID','SSID','level']
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n'
	output_lines = [] 
	for row in array:
		try:
			if len(row['data']['SCAN_RESULTS']) > 0:
				for result in row['data']['SCAN_RESULTS']:
					temp = '"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ','
					try:
						temp += '"' + result['BSSID'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + result['SSID'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += str(result['level'])
					except KeyError: pass
					output_lines.append(temp)		
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',,,,')
		except KeyError:
			output_lines.append('"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',,,,')

	return output + '\n'.join(output_lines)
					

def bluetooth_to_csv(array, output):
	#print header
	fields = ['user','data.TIMESTAMP','address','class','RSSI','name'] 
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n' 
	output_lines = []
	for row in array:
		try:
			if len(row['data']['DEVICES']) > 0:
				for device in row['data']['DEVICES']:
					temp = '"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ','
					try:
						temp += '"' + device['android_bluetooth_device_extra_DEVICE']['mAddress'] + '",'
					except KeyError: temp+= '"",'
					try: 
						temp += str(device['android_bluetooth_device_extra_CLASS']['mClass']) + ','
					except KeyError: temp += ','
					try:
						temp += str(device['android_bluetooth_device_extra_RSSI']) + ','
					except KeyError: temp += ','
					try:
						temp += '"' + device['android_bluetooth_device_extra_NAME'] + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',,,,')
		except KeyError:
			output_lines.append('"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',,,,')
			
	#return output
	return output + '\n'.join(output_lines)

def location_to_csv(array, output):
	#print header
	fields = ['user', 'data.TIMESTAMP', 'latitude','longitude','provider','accuracy']
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n' 
	for row in array:
		output += '"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',' 
		try:
			output += str(row['data']['LOCATION']['geojson']['coordinates'][0]) + ',' +\
			str(row['data']['LOCATION']['geojson']['coordinates'][1]) + ','
		except KeyError: output += ',,'
		try:
			output += '"' + row['data']['LOCATION']['mProvider'] + '",'
		except KeyError: output += ','
		try:
			output += str(row['data']['LOCATION']['mAccuracy']) + '\n'
		except KeyError: output += '\n'

	return output
			
def calllog_to_csv(array, output):
	#print header
	fields = ['user', 'data.TIMESTAMP', 'data.name', 'data.duration','data.number','data.type']
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n' 
	for row in array:
		output += row['user'] + ',' + str(row['data']['TIMESTAMP']) + ','
		try: 
			output += row['data']['name'] + ','
		except KeyError: output += '"",'
		try:
			output += str(row['data']['duration']) + ','
		except KeyError: output += ','
		try:
			output += row['data']['number'] + ','
		except KeyError: output += ','
		try:
			output += str(row['data']['type'])
		except KeyError: pass
		output += '\n'
	
	return output

def sms_to_csv(array, output):
	#print header
	fields = ['user', 'data.TIMESTAMP', 'data.read', 'data.address','data.type']
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n' 
	for row in array:
		output += row['user'] + ',' + str(row['data']['TIMESTAMP']) + ','
		try: 
			output+= str(row['data']['read']) + ','
		except KeyError: output += ','
		try: 
			output += row['data']['address'] + ','
		except KeyError: output += '"",'
		try:
			output += str(row['data']['type'])
		except KeyError: pass
		output += '\n'
	return output 
		

PHONE_DATA_SETTINGS = {\
	'bluetooth':{\
		'scope':'connector_raw.bluetooth',
		'collection':'edu_mit_media_funf_probe_builtin_BluetoothProbe',
		'default_fields':{\
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
			'data.DEVICES.android_bluetooth_device_extra_DEVICE.mAddress':1,\
			'data.DEVICES.android_bluetooth_device_extra_CLASS.mClass':1,\
			'data.DEVICES.android_bluetooth_device_extra_RSSI':1,\
			'data.DEVICES.android_bluetooth_device_extra_NAME':1}},
	'location':{\
		'scope':'connector_raw.location',
		'collection':'edu_mit_media_funf_probe_builtin_LocationProbe',
		'default_fields':{\
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
			'data.LOCATION.geojson.coordinates':1,\
			'data.LOCATION.mProvider':1,\
			'data.LOCATION.mAccuracy':1}},
	'wifi':{\
		'scope':'connector_raw.wifi',
		'collection':'edu_mit_media_funf_probe_builtin_WifiProbe',
		'default_fields':{\
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
			'data.SCAN_RESULTS.BSSID':1,\
			'data.SCAN_RESULTS.SSID':1,\
			'data.SCAN_RESULTS.level':1}},
	'calllog':{\
		'scope':'connector_raw.calllog',\
		'collection':'edu_mit_media_funf_probe_builtin_CallLogProbe',
		'default_fields':{\
			'user':1,'data.TIMESTAMP':1,'_id':1,\
			'data.name':1,\
			'data.duration':1,\
			'data.number':1,\
			'data.type':1}},
	'sms':{\
		'scope':'connector_raw.sms',\
		'collection':'edu_mit_media_funf_probe_builtin_SMSProbe',
		'default_fields':{\
			'user':1,'data.TIMESTAMP':1,'_id':1,\
			'data.read':1,\
			'data.address':1,\
			'data.type':1}}

	}

FACEBOOK_DATA_SETTINGS = {\
	'likes':{\
		'scope':'connector_raw.likes',
		'collection':'dk_dtu_compute_facebook_likes',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'data.category':1,\
			'facebook_id':1}}
	}
