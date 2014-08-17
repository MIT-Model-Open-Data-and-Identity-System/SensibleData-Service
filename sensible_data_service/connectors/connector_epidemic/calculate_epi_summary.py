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

#WAVES_STRING = '1406578700!fe05bcdc,0.015,S,36,108,S,120,1;1407580200!ad782ecd,0.015,I,36,108,S,120,2'
WAVES_STRING = '1406733000!fe05bcdc,0.015,I,360,1080,R,120,1;1407718800!deadbeef,0.015,RA_0.3,360,1080,R,120,2'
#WAVES_STRING = '1407580200!ad782ecd,0.015,I,36,108,S,120,2'
#WAVES_STRING = '1407999869!cc5a0c50,0.0225,S,36,108,R,2,9'


def calculate_epi_summary():
	this_path = os.path.split(os.path.realpath(__file__))[0] + '/'



	db = db_wrapper.DatabaseHelper()
	waves = read_waves()
	an = anonymizer.Anonymizer()
	inventory = device_inventory.DeviceInventory()
	localtz = pytz.timezone('Europe/Copenhagen')

	f = open(this_path+'epi_summary.json', 'w')

	print waves
	states = defaultdict(lambda: defaultdict(set))

	for wave in sorted(waves):
		print wave
		last_id = 0
		next_wave_begins = waves[wave]['next_wave_begins']

		while True:
			cur = db.retrieve(params={'limit':100000, 'sortby':'timestamp', 'order':1, 'after': last_id, 'start_date': wave, 'end_date': next_wave_begins}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
			if cur.rowcount == 0: break
			last_id += 1
			for row in cur:
				try:
					if row['timestamp_added'] < row['timestamp'] : continue
					user = row['user']
					data = row['data']
					data = json.loads(base64.b64decode(data))
					#if not data['wave_no'] == int(waves[wave]['wave_no']): continue
					timestamp = data['TIMESTAMP']
					date = localtz.localize(datetime.datetime.fromtimestamp(timestamp)).date()
					state = data['self_state']
					#try: side_effects_lost_points = int(data['side_effects_lost_points'])
					#except: continue
						#print user, timestamp, state, side_effects_lost_points, date
					#if state == 'V' and side_effects_lost_points > 0: state = 'VS'
					states[user][date].add(state)
				except: continue




		
	user_day_states = defaultdict(lambda: defaultdict(str)) #final state for user in given day
	all_users_in_day = defaultdict(int)


	all_days = set()
	all_users = set()

	for user in states:
		all_users.add(user)
		for date in states[user]:
			if 'I' in states[user][date]: user_day_state = 'I'
			elif 'E' in states[user][date]: user_day_state = 'I'
			elif 'VS' in states[user][date]: user_day_state = 'VS'
			elif 'V' in states[user][date]: user_day_state = 'V'
			elif 'S' in states[user][date]: user_day_state = 'S'
			else: continue
			
			user_day_states[user][date] = user_day_state
			all_users_in_day[date] += 1


	global_stats = defaultdict(lambda: defaultdict(float)) #for given day, how many users with given final state
	

	for user in user_day_states:
		for date in user_day_states[user]:
			all_days.add(date)
			global_stats[date][user_day_states[user][date]] += 1


	for date in global_stats:
		for status in global_stats[date]:
			global_stats[date][status] /= float(all_users_in_day[date])
			print date, status, global_stats[date][status]


	interactions = defaultdict(set)

	for wave in sorted(waves):
		last_id = 0
		next_wave_begins = waves[wave]['next_wave_begins']

		while True:
			cur = db.retrieve(params={'limit':100000, 'sortby':'timestamp', 'order':1, 'after': last_id, 'start_date': wave, 'end_date': next_wave_begins}, collection='edu_mit_media_funf_probe_builtin_BluetoothProbe', roles='')
			if cur.rowcount == 0: break
			last_id += 1
			for row in cur:
				if row['timestamp_added'] < row['timestamp'] : continue
				user = row['user']
				timestamp = row['timestamp']
				bt_mac = row['bt_mac']
				if bt_mac == '-1': continue

				userB = inventory.mapBtToUser(bt_mac, long(timestamp.strftime('%s')))
				if userB == bt_mac: continue

				interactions[user].add(timestamp.strftime('%s')+'_'+userB)
		
	for user in all_users:
		infected_interactions = defaultdict(set)
		vaccinated_interactions = defaultdict(set)
		vaccinated_side_interactions = defaultdict(set)
		susceptible_interactions = defaultdict(set)
		for interaction in interactions[user]:
			t = long(interaction.split('_')[0])/int(300)
			tt = long(interaction.split('_')[0])
			date = localtz.localize(datetime.datetime.fromtimestamp(tt)).date()
			userB = interaction.split('_')[1]
			all_days.add(date)
			if user_day_states[userB][date] == 'I': infected_interactions[date].add(userB)
			if user_day_states[userB][date] == 'VS': vaccinated_side_interactions[date].add(userB)
			if user_day_states[userB][date] == 'V': vaccinated_interactions[date].add(userB)
			if user_day_states[userB][date] == 'S': susceptible_interactions[date].add(userB)


		user_dict = {}
		user_dict['user'] = user
		user_dict['values'] = {}
		for day in sorted(all_days):
			if day < (datetime.datetime.now().date() + datetime.timedelta(days=-4)): continue
			all_l = float(len(infected_interactions[day]) + len(vaccinated_interactions[day]) + len(vaccinated_side_interactions[day]) + len(susceptible_interactions[day]))
			
			user_dict['values'][str(day)] = {}
			if all_l == 0:
				user_dict['values'][str(day)]['infected_interactions'] = 0
				user_dict['values'][str(day)]['vaccinated_interactions'] = 0
				user_dict['values'][str(day)]['vaccinated_side_interactions'] = 0
				user_dict['values'][str(day)]['susceptible_interactions'] = 0
			else:
				user_dict['values'][str(day)]['infected_interactions'] = len(infected_interactions[day])/all_l
				user_dict['values'][str(day)]['vaccinated_interactions'] = len(vaccinated_interactions[day])/all_l
				user_dict['values'][str(day)]['vaccinated_side_interactions'] = len(vaccinated_side_interactions[day])/all_l
				user_dict['values'][str(day)]['susceptible_interactions'] = len(susceptible_interactions[day])/all_l

			user_dict['values'][str(day)]['infected_all'] = global_stats[day]['I']
			user_dict['values'][str(day)]['vaccinated_all'] = global_stats[day]['V']
			user_dict['values'][str(day)]['vaccinated_side_all'] = global_stats[day]['VS']
			user_dict['values'][str(day)]['susceptible_all'] = global_stats[day]['S']
			user_dict['values'][str(day)]['day'] = str(day)

		f.write(json.dumps(user_dict) + '\n')
	f.close()


def calculate_epi_summary_OLD():

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
