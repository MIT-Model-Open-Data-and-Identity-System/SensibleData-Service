from sensible_audit import audit
from utils import db_wrapper
import base64
import json
import datetime

log = audit.getLogger(__name__)

USER = '725188ac89900e25dffce6454379e5'

def analyse_epidemic():
	db = db_wrapper.DatabaseHelper()
	#cur = db.retrieve(params={'limit':1000, 'sortby':'timestamp', 'order':-1, 'where': {'user':[USER]}}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
	cur = db.retrieve(params={'limit':100000, 'sortby':'timestamp', 'order':-1}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
	lt = 0
	for row in cur:
		data = json.loads(base64.b64decode(row['data']))
		user = row['user']
		timestamp = row['timestamp']
		timestamp_2 = data['TIMESTAMP']

		#if not user == '1e275e63cbe172d04d568e9c2b00ba': continue
		#if not row['device_id'] == '1be5e8c905c3f2dbad9642aa449ee779': continue
		#if not row['device_id'] == '54b8a08c7538e8f8873387a25139c786': continue
		#if not user == 'a5a21108856c86bbee025c40bdf05a': continue


#		print user, timestamp, timestamp_2, lt - timestamp_2, data['self_state'], data['infected_tag'], data['to_recover_time'],
		try: print data['state']
	#	except: print ''
		except: pass
		lt = timestamp_2
		#if timestamp < datetime.datetime(2014, 07, 29): continue
