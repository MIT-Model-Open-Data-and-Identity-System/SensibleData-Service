from collections import OrderedDict
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


PHONE_DATA_SETTINGS = {\
	'bluetooth':{\
		'scope':'connector_raw.bluetooth',
		'collection':'edu_mit_media_funf_probe_builtin_BluetoothProbe',
		'default_fields':['id','user','timestamp','class','bt_mac','name','rssi']},
	'location':{\
		'scope':'connector_raw.location',
		'collection':'edu_mit_media_funf_probe_builtin_LocationProbe',
		'default_fields':['id','user','timestamp','lat','lon','accuracy','provider']},
	'wifi':{\
		'scope':'connector_raw.wifi',
		'collection':'edu_mit_media_funf_probe_builtin_WifiProbe',
		'default_fields':['id','user','timestamp','bssid','ssid','level']},
	'calllog':{\
		'scope':'connector_raw.calllog',\
		'collection':'edu_mit_media_funf_probe_builtin_CallLogProbe',
		'default_fields':['id','user','timestamp','number','duration','type']},
	'sms':{\
		'scope':'connector_raw.sms',\
		'collection':'edu_mit_media_funf_probe_builtin_SMSProbe',
		'default_fields':['id','user','timestamp','address','body','type']},
	'cell':{\
		'scope':'connector_raw.cell',\
		'collection':'edu_mit_media_funf_probe_builtin_CellProbe',
		'default_fields':['id','user','timestamp','cid','lac','psc', 'type']},
	'contact':{\
		'scope':'connector_raw.contact',\
		'collection':'edu_mit_media_funf_probe_builtin_ContactProbe',
		'default_fields':['id','user','timestamp','contact_id','last_time_contacted','starred', 'times_contacted', 'mimetype', 'data1']},
	'hardwareinfo':{\
		'scope':'connector_raw.hardwareinfo',\
		'collection':'edu_mit_media_funf_probe_builtin_CellProbe',
		'default_fields':['id','user','timestamp','android_id','bt_mac','brand', 'device_id', 'model', 'wifi_mac']},

	'screen':{\
		'scope':'connector_raw.screen',\
		'collection':'edu_mit_media_funf_probe_builtin_ScreenProbe',
		'default_fields':['id','user','timestamp','screen_on']},

	'timeoffset':{\
		'scope':'connector_raw.timeoffset',\
		'collection':'edu_mit_media_funf_probe_builtin_TimeOffsetProbe',
		'default_fields':['id','user','timestamp','timeoffest']},

	'experience_sampling': {
		'scope': 'connector_raw.experience_sampling',
		'collection': 'edu_mit_media_funf_probe_builtin_ExperienceSamplingProbe',
		'default_fields': ['timestamp', 'user', 'answer', 'answer_type', 'question_type']
	}

	}

FACEBOOK_DATA_SETTINGS = {\
	'likes':{\
		'scope':'connector_raw.likes',
		'collection':'dk_dtu_compute_facebook_likes',
		'default_fields':['id','user','timestamp','facebook_id','data_type', 'data']},
	'friends':{\
		'scope':'connector_raw.friends',
		'collection':'dk_dtu_compute_facebook_friends',
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},
	'friendlists':{\
		'scope':'connector_raw.friendlists',
		'collection':'dk_dtu_compute_facebook_friendlists',
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'birthday':{\
		'scope':'connector_raw.birthday',
		'collection':'dk_dtu_compute_facebook_birthday',
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'education':{\
		'scope':'connector_raw.education',
		'collection':'dk_dtu_compute_facebook_education', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'groups':{\
		'scope':'connector_raw.groups',
		'collection':'dk_dtu_compute_facebook_groups', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'hometown':{\
		'scope':'connector_raw.hometown',
		'collection':'dk_dtu_compute_facebook_hometown', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'interests':{\
		'scope':'connector_raw.interests',
		'collection':'dk_dtu_compute_facebook_interests', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'locationfacebook':{\
		'scope':'connector_raw.locationfacebook',
		'collection':'dk_dtu_compute_facebook_location', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'political':{\
		'scope':'connector_raw.political',
		'collection':'dk_dtu_compute_facebook_political', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'religion':{\
		'scope':'connector_raw.religion',
		'collection':'dk_dtu_compute_facebook_religion', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'work':{\
		'scope':'connector_raw.work',
		'collection':'dk_dtu_compute_facebook_work', 
		'default_fields':['id','user','timestamp','facebook_id','data_type','data']},

	'statuses': {\
                'scope':'connector_raw.statuses',
                'collection':'dk_dtu_compute_facebook_statuses',
                'default_fields':['id','user','timestamp','facebook_id','data_type','data']},
	'feed':{\
                'scope':'connector_raw.feed',
                'collection':'dk_dtu_compute_facebook_feed',
                'default_fields':['id','user','timestamp','facebook_id','data_type','data']}

	}

QUESTIONNAIRE_DATA_SETTINGS = {\
	'questionnaire':{\
		'scope':'connector_raw.questionnaire',
		'collection':'dk_dtu_compute_questionnaire',
		'default_fields':['id','user','timestamp','variable_name','response', 'form_version']}
}
