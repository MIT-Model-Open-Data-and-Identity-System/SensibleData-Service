def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	if string == 'true': return True
	return False

PHONE_DATA_SETTINGS = {\
	'bluetooth':{\
		'scope':'connector_raw.bluetooth',
		'collection':'edu_mit_media_funf_probe_builtin_BluetoothProbe',
		'default_fields':{\
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
			'data.DEVICES':1}},
	'location':{\
		'scope':'connector_raw.location',
		'collection':'edu_mit_media_funf_probe_builtin_LocationProbe',
		'default_fields':{\
			'user':1,\
			'data.TIMESTAMP':1,\
			'_id':1,\
			'data.LOCATION.geojson.coordinates':1,\
			'data.LOCATION.mProvider':1,\
			'data.LOCATION.mAccuracy':1}}
	}
