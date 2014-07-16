from Crypto.Cipher import AES
from Crypto import Random
from utils import SECURE_settings
import bson.json_util as json
from operator import getitem
from collections import defaultdict
import pdb
class Anonymizer(object):

	BS = 16

	def __init__(self):
		pass
	

	def pad(self, s):
		return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

	def unpad(self, s):
		return s[0:-ord(s[-1])]


	def add_keys(self, d, l, c=None):
		if len(l) > 1:
			d[l[0]] = _d = {}
			d[l[0]] = d.get(l[0], {})
			self.add_keys(d[l[0]], l[1:], c)
		else:
			d[l[0]] = c


	def merge(self, a, b, path=None):
		if path is None: path = []
		for key in b:
			if key in a:
				if isinstance(a[key], dict) and isinstance(b[key], dict):
					self.merge(a[key], b[key], path + [str(key)])
				elif a[key] == b[key]:
					pass # same leaf value
				else:
					raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
			else:
				a[key] = b[key]
				
		return a


	def anonymizeValue(self, key_v, value):
		try:
			key = SECURE_settings.VALUE_KEYS[key_v]
		except KeyError:
			return value
		self.key = key.decode("hex")
		return self.encrypt(value)
	
	def deanonymizeValue(self, key_v, value):
		try:
			key = SECURE_settings.VALUE_KEYS[key_v]
		except KeyError:
			return value
		self.key = key.decode("hex")
		return self.decrypt(value)

	def anonymizeDocument(self, document, probe):
		try:
			key = SECURE_settings.PROBE_KEYS[probe]
		except KeyError:
			return document
		self.key = key.decode("hex")
		#TODO: figure out the configuration setup for the probes


		if probe == 'edu_mit_media_funf_probe_builtin_WifiProbe': self.anonymizeWifi(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_BluetoothProbe': self.anonymizeBluetooth(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_LocationProbe': self.anonymizeLocation(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_CallLogProbe': self.anonymizeCallLog(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_SMSProbe': self.anonymizeSMSProbe(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_HardwareInfoProbe': self.anonymizeHardwareProbe(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_ContactProbe': self.anonymizeContactProbe(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_BatteryProbe': document = self.anonymizeBatteryProbe(document)
		elif probe == 'edu_mit_media_funf_probe_builtin_ExperienceSamplingProbe': document = self.anonymizeExperienceSamplingProbe(document)
		
		
		
		elif probe == 'dk_dtu_compute_facebook_facebook_id': document = self.anonymizeFacebookId(document)
		elif probe == 'dk_dtu_compute_facebook_friendlists': self.anonymizeFacebookFriendlists(document)
		elif probe == 'dk_dtu_compute_facebook_friends': self.anonymizeFacebookFriends(document)
		elif probe == 'dk_dtu_compute_facebook_friendrequests': self.anonymizeFacebookFriendrequests(document)
		elif probe == 'dk_dtu_compute_facebook_groups': self.anonymizeFacebookGroups(document)
		elif probe == 'dk_dtu_compute_facebook_likes': self.anonymizeFacebookLikes(document)
		elif probe == 'dk_dtu_compute_facebook_feed': document = self.anonymizeFacebookFeed(document)
		elif probe == 'dk_dtu_compute_facebook_statuses': document = self.anonymizeFacebookStatuses(document)
		elif probe == 'dk_dtu_compute_facebook_education': document = self.anonymizeFacebookEducation(document)
		elif probe == 'dk_dtu_compute_facebook_locations': document = self.anonymizeFacebookLocations(document)
		elif probe == 'dk_dtu_compute_facebook_work': document = self.anonymizeFacebookWork(document)
		
		return document	
	
	def deanonymizeDocument(self, document, probe):
		try:
			key = SECURE_settings.PROBE_KEYS[probe]
		except KeyError:
			return document
		self.key = key.decode("hex")

		if probe == 'edu_mit_media_funf_probe_builtin_BluetoothProbe': document = self.deanonymizeBluetooth(document)
		elif probe == 'dk_dtu_compute_facebook_friends': document = self.deanonymizeFacebookFriendsConnections(document)
		return document
				
	def anonymizeExperienceSamplingProbe(self, document):
		if document['answer']['question_type'] == 'SOCIAL_RATE_TWO_FRIENDS' or document['answer']['question_type'] == 'SOCIAL_CLOSER_FRIEND':
			document['answer']['friend_one_uid'] = self.encrypt(document['answer']['friend_one_uid'])
			document['answer']['friend_two_uid'] = self.encrypt(document['answer']['friend_two_uid'])
		#elif document['answer']['question_type'] ==
		return document

	def anonymizeBatteryProbe(self, document):
		document.pop('icon-small', None)
		document.pop('invalid_charger',None)
		document.pop('scale',None)
		document.pop('voltage',None)
		document.pop('technology',None)
		document.pop('present',None)
		return document
		
	
	def anonymizeWifi(self, document):
		for scan in document['SCAN_RESULTS']:
			#scan['SSID'] = self.encrypt(scan['SSID'])
			#scan['BSSID'] = self.encrypt(scan['BSSID'])
			scan.pop('wifiSsid', None)
	
	def anonymizeBluetooth(self, document):
		for device in document['DEVICES']:
			device['android_bluetooth_device_extra_DEVICE']['mAddress'] = self.encrypt(device['android_bluetooth_device_extra_DEVICE']['mAddress'].lower())
			try:
				device['android_bluetooth_device_extra_NAME'] = self.encrypt(device['android_bluetooth_device_extra_NAME'])
			except KeyError: pass
	
		
	def deanonymizeBluetooth(self, documents):
		addresses = {}
		names = {}
		if type(documents) == dict:
			documents = [documents]

		for document in documents:
			enc_mac = str(document['bt_mac'])
			try:
				document['bt_mac'] = addresses[enc_mac]
			except KeyError:
				dec_mac = self.decrypt(enc_mac)
				addresses[enc_mac] = dec_mac
				document['bt_mac'] = dec_mac
			try:
				enc_name = ''
				try:
					enc_name = str(document['name'])
				except KeyError: continue
				document['name'] = names[enc_name]
			except KeyError:
				dec_name = self.decrypt(enc_name)
				names[enc_name] = dec_name
				document['name'] = dec_name
		
		#if len(documents) > 0:
		#	documents[0]['addresses'] = addresses
		#	documents[0]['names'] = names
		return documents

	def anonymizeLocation(self, document):
		lat = document['LOCATION']['mLatitude']
		lon = document['LOCATION']['mLongitude']
		geoJson = dict()
		geoJson['type'] = "Point"
		geoJson['coordinates'] = []
		geoJson['coordinates'].append(lat)
		geoJson['coordinates'].append(lon)
	
		document['LOCATION']['geojson'] = geoJson
	
	def anonymizeCallLog(self, document):
		try:
			if len(document['name']) > 0:
				document['name'] = json.loads(document['name'])["ONE_WAY_HASH"]
			document['numbertype'] = json.loads(document['numbertype'])["ONE_WAY_HASH"]
			document['number'] = json.loads(document['number'])["ONE_WAY_HASH"]
		except KeyError: pass
	
	def anonymizeSMSProbe(self, document):
		try:
			if len(document['body']) > 0:
				document['body'] = json.loads(document['body'])["ONE_WAY_HASH"]
			if len(document['address']) > 0:
				document['address'] = json.loads(document['address'])["ONE_WAY_HASH"]
			if len(document['person']) > 0:
				document['person'] = json.loads(document['person'])["ONE_WAY_HASH"]
		except KeyError: pass
		except ValueError: pass		

	def anonymizeHardwareProbe(self, document):
		document['BLUETOOTH_MAC'] = self.anonymizeValue('bluetooth_mac', document['BLUETOOTH_MAC'].lower()) #the same as bluetooth probe
		document['WIFI_MAC'] = self.anonymizeValue('wifi_mac', document['WIFI_MAC'].lower()) #the same as wifi probe
		document['ANDROID_ID'] = self.anonymizeValue('android_id', document['ANDROID_ID'].lower()) #the same as wifi probe
		document['DEVICE_ID'] = self.anonymizeValue('device_id', document['DEVICE_ID'].lower()) #the same as wifi probe

	def anonymizeContactProbe(self, document):
		for entry in document['CONTACT_DATA']:
			for key in entry:	
				try:
					if 'ONE_WAY_HASH' in entry[key]:
						entry[key] = json.loads(entry[key])["ONE_WAY_HASH"]
				except TypeError: pass
		try:
			document['display_name'] = json.loads(document['display_name'])["ONE_WAY_HASH"]
		except KeyError: pass

	def anonymizeFacebookFriendlists(self, document):
		for ls in document:
			ls['id'] = self.encrypt(ls['id'])

	def anonymizeFacebookFriends(self, document):
		for ps in document:
			ps['id'] = self.encrypt(ps['id'])
			ps['name'] = self.encrypt(ps['name'])
	
	def deanonymizeFacebookFriendsConnections(self, document):
		response = {'connections':[], 'friends':[]}
		cache = {}
		for friend in document['friends']:
			cache[friend] = self.decrypt(friend)
		response['friends'] = cache.values()
		for dyad in document['connections']:
			response['connections'].append([cache[dyad[0]], cache[dyad[1]]])
		return response
		
	
	def anonymizeFacebookFriendrequests(self, document):
		for rq in document:
			rq['to']['id'] = self.encrypt(rq['to']['id'])
			rq['to']['name'] = self.encrypt(rq['to']['name'])
			rq['from']['id'] = self.encrypt(rq['from']['id'])
			rq['from']['name'] = self.encrypt(rq['from']['name'])
	
	def anonymizeFacebookGroups(self, document):
		for gr in document:
			gr['id'] = self.encrypt(gr['id'])
			gr['name'] = self.encrypt(gr['name'])
	
	def anonymizeFacebookLikes(self, document):
		for lk in document:
			lk['id'] = self.encrypt(lk['id'])
			lk['name'] = self.encrypt(lk['name'])
	
	def anonymizeFacebookId(self, document):
		return self.anonymizeValue('facebook_id', document)

	
	def anonymizeFacebookFeed(self, document):
		allowed_keys = ['status_type', 'updated_time', 'type', 'created_time']
		output = []
		self.anonymizeFacebookFeedWorker(document, [], allowed_keys, output)
		dd = reduce(self.merge, output)
		return dd
	

	def anonymizeFacebookFeedWorker(self, document, keys, allowed_keys, output):
		if type(document) == type([]):
			for jj, item in enumerate(document):
				t_keys = list(keys)
				t_keys.append(str(jj))
				self.anonymizeFacebookFeedWorker(item, t_keys, allowed_keys, output)
		elif type(document) == type({}):
			for key, value in document.items():
				t_keys = list(keys)
				t_keys.append(key)
				self.anonymizeFacebookFeedWorker(value, t_keys, allowed_keys, output)
		else:
			if not keys[-1] in allowed_keys: document = self.encrypt(document)
			d = {}
			self.add_keys(d, keys, document)
			output.append(d)
	
	def anonymizeFacebookStatuses(self, document):
		allowed_keys = ['status_type', 'updated_time', 'type', 'created_time', 'latitude', 'longitude']
		output = []
		self.anonymizeFacebookStatusesWorker(document, [], allowed_keys, output)
		dd = reduce(self.merge, output)
		return dd
	

	def anonymizeFacebookStatusesWorker(self, document, keys, allowed_keys, output):
		if type(document) == type([]):
			for jj, item in enumerate(document):
				t_keys = list(keys)
				t_keys.append(str(jj))
				self.anonymizeFacebookStatusesWorker(item, t_keys, allowed_keys, output)
		elif type(document) == type({}):
			for key, value in document.items():
				t_keys = list(keys)
				t_keys.append(key)
				self.anonymizeFacebookStatusesWorker(value, t_keys, allowed_keys, output)
		else:
			if not keys[-1] in allowed_keys: document = self.encrypt(document)
			d = {}
			self.add_keys(d, keys, document)
			output.append(d)
	
	
	def anonymizeFacebookEducation(self, document):
		for pl in document:
			try:
				for cl in pl['classes']:
					try:
						cl['id'] = self.encrypt(cl['id'])
						for ps in cl['with']:
							ps['id'] = self.encrypt(ps['id'])
							ps['name'] = self.encrypt(ps['name'])
					except KeyError: continue
			except KeyError: continue

		return document
	
	
	def anonymizeFacebookLocations(self, document):
		allowed_keys = ['status_type', 'updated_time', 'type', 'created_time', 'latitude', 'longitude']
		output = []
		self.anonymizeFacebookLocationsWorker(document, [], allowed_keys, output)
		dd = reduce(self.merge, output)
		return dd
	

	def anonymizeFacebookLocationsWorker(self, document, keys, allowed_keys, output):
		if type(document) == type([]):
			for jj, item in enumerate(document):
				t_keys = list(keys)
				t_keys.append(str(jj))
				self.anonymizeFacebookLocationsWorker(item, t_keys, allowed_keys, output)
		elif type(document) == type({}):
			for key, value in document.items():
				t_keys = list(keys)
				t_keys.append(key)
				self.anonymizeFacebookLocationsWorker(value, t_keys, allowed_keys, output)
		else:
			if not keys[-1] in allowed_keys: document = self.encrypt(document)
			d = {}
			self.add_keys(d, keys, document)
			output.append(d)
	
	def anonymizeFacebookWork(self, document):
		for pl in document:
			try:
				for cl in pl['projects']:
					try:
						cl['id'] = self.encrypt(cl['id'])
						for ps in cl['with']:
							ps['id'] = self.encrypt(ps['id'])
							ps['name'] = self.encrypt(ps['name'])
					except KeyError: continue
			except KeyError: continue

		return document

	def encrypt(self, raw):
		raw = unicode(raw).encode('utf-8')
		raw = self.pad(raw)
		#we use fixed iv to have consistent encryption
		iv = SECURE_settings.IV['iv']
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return (cipher.encrypt(raw)).encode("hex")

	def decrypt(self, enc):
		try: 
			temp = enc.strip().decode("hex")
			iv = SECURE_settings.IV['iv']
			cipher = AES.new(self.key, AES.MODE_CBC, iv)
			return self.unpad(cipher.decrypt(temp))
		except Exception: #the data might already be decrypted, just return the original
			return '+' + enc
