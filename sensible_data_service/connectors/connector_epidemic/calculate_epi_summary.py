from sensible_audit import audit
from utils import db_wrapper
import base64
import json
import datetime
from collections import defaultdict
from anonymizer import anonymizer
from connectors.connector_funf import device_inventory
import pytz
import os


log = audit.getLogger(__name__)

WAVES_STRING = '1406578700!fe05bcdc,0.015,S,36,108,S,120,1;1407580200!ad782ecd,0.015,I,36,108,S,120,2'
#WAVES_STRING = '1407580200!ad782ecd,0.015,I,36,108,S,120,2'
#WAVES_STRING = '1406578700!Nexus,0.015,S,36,108,S,120,1'

def calculate_epi_summary():

	this_path = os.path.split(os.path.realpath(__file__))[0] + '/'

	db = db_wrapper.DatabaseHelper()
	waves = read_waves()
	an = anonymizer.Anonymizer()
	inventory = device_inventory.DeviceInventory()
	localtz = pytz.timezone('Europe/Copenhagen')

	f = open(this_path+'epi_summary.json', 'w')

	for wave in sorted(waves):
		last_id = 0
		next_wave_begins = waves[wave]['next_wave_begins']
		interactions = defaultdict(set)

		while True:
			cur = db.retrieve(params={'limit':100000, 'sortby':'timestamp', 'order':1, 'after': last_id, 'start_date': wave, 'end_date': next_wave_begins}, collection='edu_mit_media_funf_probe_builtin_BluetoothProbe', roles='')
			if cur.rowcount == 0: break
			last_id += 1
			for row in cur:
				if row['timestamp_added'] < row['timestamp'] : continue
				user = row['user']
				timestamp = row['timestamp']
				bt_mac = row['bt_mac']
				bt_name = row['name']
				if bt_mac == '-1': continue

				if bt_name: bt_name = an.deanonymizeValue('bluetooth_name', bt_name)
				else: bt_name = ''
				userB = inventory.mapBtToUser(bt_mac, long(timestamp.strftime('%s')))
				if userB == bt_mac: continue

				interactions[user].add(timestamp.strftime('%s')+'_'+userB+'_'+bt_name.decode('utf-8'))
			

		for user in interactions:
			save_string = ''
			infected_interactions = defaultdict(set)
			vaccinated_interactions = defaultdict(set)
			susceptible_interactions = defaultdict(set)
			all_days = set()
			for interaction in interactions[user]:
				t = long(interaction.split('_')[0])/int(300)
				tt = long(interaction.split('_')[0])
				date = localtz.localize(datetime.datetime.fromtimestamp(tt)).date()
				userB = interaction.split('_')[1]
				name = interaction.split('_')[2]
				all_days.add(date)
				if name.endswith(waves[wave]['infected_tag'].decode('utf-8')): infected_interactions[date].add(str(t) + userB)
				elif name.endswith(waves[wave]['vaccinated_tag']): vaccinated_interactions[date].add(str(t) + userB)
				else: susceptible_interactions[date].add(str(t) + userB)
			user_dict = {}
			user_dict['user'] = user
			user_dict['values'] = {}
			for day in sorted(all_days):
				user_dict['values'][str(day)] = {}
				user_dict['values'][str(day)]['wave_no'] = int(waves[wave]['wave_no'])
				user_dict['values'][str(day)]['infected_interactions'] = len(infected_interactions[day])
				user_dict['values'][str(day)]['vaccinated_interactions'] = len(vaccinated_interactions[day])
				user_dict['values'][str(day)]['susceptible_interactions'] = len(susceptible_interactions[day])

			f.write(json.dumps(user_dict) + '\n')
	f.close()


def read_waves():
	waves_list = WAVES_STRING.split(';')
	waves = defaultdict(lambda: defaultdict(str))

	for wave in waves_list:
		wave_start = long(wave.split('!')[0])
		infected_tag = wave.split('!')[1].split(',')[0]
		wave_no = wave.split('!')[1].split(',')[7]
		waves[wave_start]['infected_tag'] = infected_tag
		waves[wave_start]['vaccinated_tag'] = infected_tag + '_VAC'
		waves[wave_start]['wave_no'] = wave_no
		

	next_wave_begins = -1

	for wave in sorted(waves, reverse=True):
		if next_wave_begins == -1: next_wave_begins = wave + 60 * 60 * 24 * 7
		waves[wave]['next_wave_begins'] = next_wave_begins
		next_wave_begins = wave

	return waves
