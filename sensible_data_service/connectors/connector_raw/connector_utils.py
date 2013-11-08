from collections import OrderedDict
from connectors.connector_funf import device_inventory
from bson import ObjectId

def stringify_object_ids(obj):
	if type(obj) == list:
		for elt in obj: elt = _stringify_object_ids(elt)
		return obj
	else:
		return _stringify_object_ids(obj)

def _stringify_object_ids(elt):
	try:
		if type(elt['_id']) == ObjectId:
			elt['_id'] = str(elt['_id'])
	except KeyError: pass
	return elt

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
	elif 'friends' in collection.lower():
		return friends_to_csv(array,output)
	elif 'friendlists' in collection.lower():
		return friendlists_to_csv(array,output)
	elif 'birthday' in collection.lower():
		return birthday_to_csv(array,output)
	elif 'education' in collection.lower():
		return education_to_csv(array,output)
	elif 'groups' in collection.lower():
		return groups_to_csv(array,output)
	elif 'hometown' in collection.lower():
		return hometown_to_csv(array,output)
	elif 'interests' in collection.lower():
		return interests_to_csv(array,output)
	elif 'locationfacebook' in collection.lower():
		return locationfacebook_to_csv(array,output)
	elif 'political' in collection.lower():
		return political_to_csv(array,output)
	elif 'religion' in collection.lower():
		return religion_to_csv(array,output)
	elif 'work' in collection.lower():
		return work_to_csv(array,output)
	elif 'questionnaire' in collection.lower():
		return questionnaire_to_csv(array,output)
	else:
		return 'We do not yet support csv output for ' + collection + ' data. Sorry!'

def birthday_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data','facebook_id']
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
				temp = '"' + row['user'] + '",' + str(row['timestamp']) + ',' 
				try:
					temp += '"' + row['data']+ '",'
				except KeyError: temp += '"",'
				try:
					temp += '"' + str(row['facebook_id']) + '"'
				except KeyError: temp += '""'
				output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def education_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.school.name','data.classes.name','data.type','facebook_id']
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
						temp += '"' + result['school']['name'] + '",'
						
					except KeyError: temp += '"",'
					try:
						if len(result['classes']) >= 1:
							temp=''
							for classe in result['classes']:
								temp = '"' + row['user'] + '",' + str(row['timestamp']) + ','+ '"' + result['school']['name'] + '",'+'"' + classe['name'] + '",'
								try:
									temp += '"' + result['type'] + '",'
								except KeyError: temp += '"",'
								try:
									temp += '"' + str(row['facebook_id']) + '"'
								except KeyError: temp += '""'
								output_lines.append(temp)
								
						else: 
							temp += '"",'
							try:
								temp += '"' + result['type'] + '",'
							except KeyError: temp += '"",'
							try:
								temp += '"' + str(row['facebook_id']) + '"'
							except KeyError: temp += '""'
							output_lines.append(temp)
					except KeyError: 
							temp += '"",'
							try:
								temp += '"' + result['type'] + '",'
							except KeyError: temp += '"",'
							try:
								temp += '"' + str(row['facebook_id']) + '"'
							except KeyError: temp += '""'
							output_lines.append(temp)
	
					
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)


def friends_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','facebook_id']
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
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def friendlists_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','data.name','data.list_type','facebook_id']
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
						temp += '"' + result['name'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + result['list_type'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def groups_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','facebook_id']
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
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def hometown_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','data.name','facebook_id']
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
				temp = '"' + row['user'] + '",' + str(row['timestamp']) + ',' 
				try:
					temp += '"' + row['data']['id'] + '",'
				except KeyError: temp += '"",'
				try:
					temp += '"' + row['data']['name'] + '",'
				except KeyError: temp += '"",'
				try:
					temp += '"' + str(row['facebook_id']) + '"'
				except KeyError: temp += '""'
				output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def interests_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','data.name','data.category','facebook_id']
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
						temp += '"' + result['name'] + '",'
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

def locationfacebook_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.id','data.name','facebook_id']
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
					temp = '"' + row['user'] + '",' + str(row['timestamp']) + ',' 
					try:
						temp += '"' + row['data']['id'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + row['data']['name'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def political_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data','facebook_id']
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
					temp = '"' + row['user'] + '",' + str(row['timestamp']) + ',' 
					try:
						temp += '"' + row['data'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def religion_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data','facebook_id']
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
					temp = '"' + row['user'] + '",' + str(row['timestamp']) + ',' 
					try:
						temp += '"' + row['data'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

def work_to_csv(array, output):
	#print header
	fields = ['user','timestamp','data.employer.name','facebook_id']
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
						if len(result['employer']) > 0:
							for employer in result['employer']:
								temp += '"' + employer['name'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + str(row['facebook_id']) + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,')

		except KeyError: output_lines.append('"' + row['user'] + '",' + str(row['timestamp']) + ',,,,')

		
	return output + '\n'.join(output_lines)

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
#	deviceInventory = device_inventory.DeviceInventory()
	fields = ['user','data.TIMESTAMP','address','class','RSSI','name','device_holder'] 
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
						temp += '"' + device['android_bluetooth_device_extra_NAME'] + '",'
					except KeyError: temp += '"",'
					try:
						temp += '"' + device['user'] + '"'
					except KeyError: temp += '""'
					output_lines.append(temp)
			else:
				output_lines.append('"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',"",,,"",""')
		except KeyError:
			output_lines.append('"' + row['user'] + '",' + str(row['data']['TIMESTAMP']) + ',"",,,"",""')
			
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
		
def questionnaire_to_csv(array, output):
	#print header
	fields = ['user', 'variable_name','form_version','human_readable_response','last_answered']
	for i, field in enumerate(fields):
		output += field
		if i < len(fields)-1:
			output += ','
		else:
			output += '\n' 
	output_lines = [] 
	for row in array:
		try:
			temp ='"' + row['user'] + '"' + ',' 
			try: 
				temp += '"'+ row['variable_name'] + '"' +','
			except KeyError: temp += '"",'
			try: 
				temp += '"' + row['form_version'] + '"' + ','
			except KeyError: temp += '"",'
			try:
				temp+= '"' + row['human_readable_response'].replace('"','\\"').replace('\n','\\n').replace('\r','\\n') +  '"' + ','	
			except KeyError: temp += '"",'
			try:
				temp+= '"' + row['last_answered']+ '"' + ','
			except KeyError: temp += '""'
			output_lines.append(temp)
		except KeyError: output_lines.append('"' + row['user'] + '",' +',,,,')
	return output + '\n'.join(output_lines)

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
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
			'data.name':1,\
			'data.duration':1,\
			'data.number':1,\
			'data.type':1}},
	'sms':{\
		'scope':'connector_raw.sms',\
		'collection':'edu_mit_media_funf_probe_builtin_SMSProbe',
		'default_fields':{\
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
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
			'facebook_id':1}},
	'friends':{\
		'scope':'connector_raw.friends',
		'collection':'dk_dtu_compute_facebook_friends',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'facebook_id':1}},
	'friendlists':{\
		'scope':'connector_raw.friendlists',
		'collection':'dk_dtu_compute_facebook_friendlists',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'data.name':1,\
			'data.list_type':1,\
			'facebook_id':1}},
	'birthday':{\
		'scope':'connector_raw.birthday',
		'collection':'dk_dtu_compute_facebook_birthday',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data':1,\
			'facebook_id':1}},
	'education':{\
		'scope':'connector_raw.education',
		'collection':'dk_dtu_compute_facebook_education',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.school.name':1,\
			'data.classes.name':1,\
			'data.type':1,\
			'facebook_id':1}},
	'groups':{\
		'scope':'connector_raw.groups',
		'collection':'dk_dtu_compute_facebook_groups',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'facebook_id':1}},
	'hometown':{\
		'scope':'connector_raw.hometown',
		'collection':'dk_dtu_compute_facebook_hometown',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'data.name':1,\
			'facebook_id':1}},
	'interests':{\
		'scope':'connector_raw.interests',
		'collection':'dk_dtu_compute_facebook_interests',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'data.name':1,\
			'data.category':1,\
			'facebook_id':1}},
	'locationfacebook':{\
		'scope':'connector_raw.locationfacebook',
		'collection':'dk_dtu_compute_facebook_location',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data.id':1,\
			'data.name':1,\
			'facebook_id':1}},
	'political':{\
		'scope':'connector_raw.political',
		'collection':'dk_dtu_compute_facebook_political',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data':1,\
			'facebook_id':1}},
	'religion':{\
		'scope':'connector_raw.religion',
		'collection':'dk_dtu_compute_facebook_religion',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data':1,\
			'facebook_id':1}},
	'work':{\
		'scope':'connector_raw.work',
		'collection':'dk_dtu_compute_facebook_work',
		'default_fields':{\
			'user':1,\
			'timestamp':1,\
			'data':1,\
			'facebook_id':1}}
	}

QUESTIONNAIRE_DATA_SETTINGS = {\
	'questionnaire':{\
		'scope':'connector_raw.questionnaire',
		'collection':'dk_dtu_compute_questionnaire',
		'default_fields':{\
			'user':1,\
			'variable_name':1,\
			'form_version':1,\
			'last_answered':1,\
			'human_readable_question':1,\
			'human_readable_response':1}}
}
