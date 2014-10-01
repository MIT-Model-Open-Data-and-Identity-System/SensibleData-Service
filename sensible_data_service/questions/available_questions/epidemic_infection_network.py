import base64
import calendar
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
	end = datetime.datetime(2014, 10, 6)

	for dt in rrule.rrule(rrule.DAILY, dtstart=start, until=end):
		cursor = db.retrieve(params={'limit':10000000, 'sortby':'timestamp', 'order':-1, 'start_date': calendar.timegm(dt), 'end_date': calendar.timegm(dt + datetime.timedelta(hours=23, minutes=59))}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='').fetchall()
		infection_events = []
		for doc in cursor:
			data = json.loads(base64.b64decode(doc['data']))
			if 'last_state_change' not in data: continue
			last_state_change = data['last_state_change'].split("_")
			if len(last_state_change) < 2: continue
			if last_state_change[1] != 'I': continue

			infecting_user = device_inventory.mapBtToUser(last_state_change[2], doc['timestamp']) if last_state_change[3] != 'server' else 'server'
			infection_event = InfectionEvent(infected_user=doc['username'], timestamp=time.localtime(doc['timestamp']), infecting_user = infecting_user, wave_no = data['wave_no'])
			infection_events.append(infection_event)
		InfectionEvent.bulk_create(infection_events)

