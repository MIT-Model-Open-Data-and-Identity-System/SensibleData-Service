import base64
import datetime
import json
import time
from dateutil import rrule
from connectors.connector_funf.device_inventory import DeviceInventory
from questions.models import InfectionEvent
from utils import db_wrapper

NAME = 'epidemic_infection_network'

def run():
	db = db_wrapper.DatabaseHelper()
	device_inventory = DeviceInventory()

	start = datetime.datetime(2014, 9, 8)
	end = datetime.datetime(2014, 10, 5)

	for dt in rrule.rrule(rrule.DAILY, dtstart=start, until=end):
		cursor = db.retrieve(params={'limit': 10000000, 'sortby': 'timestamp', 'order': -1, 'start_date': time.mktime(dt.timetuple()), 'end_date': time.mktime((dt + datetime.timedelta(hours=23, minutes=59)).timetuple())}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='').fetchall()
		infection_events_tuples = set([])
		for doc in cursor:
			data = json.loads(base64.b64decode(doc['data']))
			if 'last_state_change' not in data: continue
			last_state_change = data['last_state_change'].split("_")
			if len(last_state_change) < 2: continue
			if last_state_change[1] != 'I': continue

			infecting_user = device_inventory.mapBtToUser(last_state_change[2], int(last_state_change[0])) if last_state_change[3] != 'server' else 'server'
			infection_events_tuples.add((doc['user'], int(last_state_change[0]), infecting_user, data['wave_no']))
		cursor = None
		InfectionEvent.objects.bulk_create([InfectionEvent(infected_user = tup[0], timestamp = datetime.datetime.fromtimestamp(tup[1]/1e3), infecting_user = tup[2], wave_no = tup[3]) for tup in infection_events_tuples])
		print "Finished: " + str(dt)

