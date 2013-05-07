from Crypto.Cipher import AES
from Crypto import Random
from utils import SECURE_service_config
import bson.json_util as json


class Anonymizer(object):

	BS = 16

	def __init__(self):
		pass
	

	def pad(self, s):
		return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

	def unpad(self, s):
		return s[0:-ord(s[-1])]



	def anonymizeValue(self, key_v, value):
		try:
			key = SECURE_service_config.VALUE_KEYS[key_v]
		except KeyError:
			return value
		self.key = key.decode("hex")
		return self.encrypt(value)

	def anonymizeDocument(self, document, probe):
		
		try:
			key = SECURE_service_config.PROBE_KEYS[probe]
		except KeyError:
			return document
		self.key = key.decode("hex")
		#TODO: move from secure config to config


		if probe == 'edu_mit_media_funf_probe_builtin_WifiProbe': self.anonymizeWifi(document)
		if probe == 'edu_mit_media_funf_probe_builtin_BluetoothProbe': self.anonymizeBluetooth(document)
		if probe == 'edu_mit_media_funf_probe_builtin_LocationProbe': self.anonymizeLocation(document)
		if probe == 'edu_mit_media_funf_probe_builtin_CallLogProbe': self.anonymizeCallLog(document)
		if probe == 'edu_mit_media_funf_probe_builtin_SMSProbe': self.anonymizeSMSProbe(document)
		if probe == 'edu_mit_media_funf_probe_builtin_HardwareInfoProbe': self.anonymizeHardwareProbe(document)
		if probe == 'edu_mit_media_funf_probe_builtin_ContactProbe': self.anonymizeContactProbe(document)
		return document

		
	def anonymizeWifi(self, document):
		for scan in document['SCAN_RESULTS']:
			scan['SSID'] = self.encrypt(scan['SSID'])
			scan['BSSID'] = self.encrypt(scan['BSSID'])
			scan['wifiSsid'] = {}
	
	def anonymizeBluetooth(self, document):
		for device in document['DEVICES']:
			device['android_bluetooth_device_extra_DEVICE']['mAddress'] = self.encrypt(device['android_bluetooth_device_extra_DEVICE']['mAddress'].lower())
			try:
				device['android_bluetooth_device_extra_NAME'] = self.encrypt(device['android_bluetooth_device_extra_NAME'])
			except KeyError: pass
		
			
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
			document['name'] = json.loads(document['name'])["ONE_WAY_HASH"]
			document['numbertype'] = json.loads(document['numbertype'])["ONE_WAY_HASH"]
			document['number'] = json.loads(document['number'])["ONE_WAY_HASH"]
		except KeyError: pass
	
	def anonymizeSMSProbe(self, document):
		try:
			document['body'] = json.loads(document['body'])["ONE_WAY_HASH"]
			document['address'] = json.loads(document['address'])["ONE_WAY_HASH"]
			document['person'] = json.loads(document['person'])["ONE_WAY_HASH"]
		except KeyError: pass
			

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

		document['display_name'] = json.loads(document['display_name'])["ONE_WAY_HASH"]

	def encrypt(self, raw):
		raw = unicode(raw).encode('utf-8')
		raw = self.pad(raw)
		#we use fixed iv to have consistent encryption
		iv = SECURE_service_config.IV['iv']
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return (cipher.encrypt(raw)).encode("hex")

	def decrypt(self, enc):
		enc = enc.decode("hex")
		#iv = enc[:16]
		iv = SECURE_service_config.IV['iv']
		enc = enc[16:]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self.unpad(cipher.decrypt(enc))
		
