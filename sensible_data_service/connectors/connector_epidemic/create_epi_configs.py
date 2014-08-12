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
import argparse
from dateutil import parser
import hashlib
import connectors.connectors_config

args = None

def create_epi_configs():
	global args
	this_path = os.path.split(os.path.realpath(__file__))[0] + '/'
	myConnector = connectors.connectors_config.CONNECTORS['ConnectorFunf']['config']
	config_path = os.path.split(myConnector['config_path'])[0]+'/'
	args = build_django_args()

	base_config = load_base_config(this_path+'funf_config_base.json')
	debug(base_config)

	summary = load_summary(this_path+'epi_summary.json')
	debug(summary)

	for user in summary:
		epi_config = create_epi_config(base_config, summary[user])
		save_config(epi_config, config_path+'config.json_'+user)
	
	epi_config = create_epi_config(base_config, {})
	save_config(epi_config, config_path+'config.json')


def build_args():
	parser = argparse.ArgumentParser(description='Create epi config for users.')
	parser.add_argument('--user', type=str, help='user for whom to create config')
	parser.add_argument('--base_config', type=str, help='base config')
	parser.add_argument('--silent', type=str, help='suppress printing')
	parser.add_argument('--SCAN_DELTA', type=int, default=250, help='minimal distance between BT scans when the infection can happen, in seconds')
	parser.add_argument('--TIME_LIMIT', type=int, default=12*60, help='do not apply arguments from the config that are older than this limit, in minutes')
	parser.add_argument('--VIBRATE_PROBABILITY', type=float, default=0.0, help='probability of phone vibrating in every 5 minute period')
	parser.add_argument('--POPUP_PROBABILITY', type=float, default=0.0, help='probability of toast showing in every 5 minute period')
	parser.add_argument('--SILENT_NIGHT', type=bool, default=True, help='should symptoms be suppressed at night (24-8)')
	parser.add_argument('--HIDDEN_MODE', type=bool, default=True, help='suppress all user interaction and notifications')
	parser.add_argument('--SHOW_WELCOME_DIALOG', type=long, default=1409410800, help='starting when should welcome screen be shown')
	
	args = parser.parse_args()	
	return args


def load_summary(name):
	summary = {}
	for line in open(name):
		line = line.strip()
		values = json.loads(line)
		summary[values['user']] = values['values']

	return summary

class Args:
	silent = False
	SCAN_DELTA = 250
	TIME_LIMIT = 12 * 60
	VIBRATE_PROBABILITY = 0.0
	POPUP_PROBABILITY = 0.0
	SILENT_NIGHT = True
	HIDDEN_MODE = False
	SHOW_WELCOME_DIALOG = 1409410800
	SHOW_FINAL_DIALOG = 1418436000
	FINAL_DIALOG_URL = "http://www.sensible.dtu.dk/?page_id=2044"

def build_django_args():
	return Args()

def load_base_config(name):
	if not name: name = 'funf_config_base.json'
	base_config = json.loads(open(name).read())
	debug(base_config, "base config")
	return base_config

def pretty_print(v, key):
	if not type(v) == dict: print "[D] %s:"%key, v
	else: print "[D] %s:"%key, json.dumps(v, indent=4, separators=(',',': '))
	
def debug(v, key=None):
	global args
	if args.silent: return
	pretty_print(v, key)


def create_epi_config(base_config, summary):
	epi_config = base_config
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'] = [{}]
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['SCAN_DELTA'] = args.SCAN_DELTA
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['TIME_LIMIT'] = args.TIME_LIMIT
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['VIBRATE_PROBABILITY'] = args.VIBRATE_PROBABILITY
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['POPUP_PROBABILITY'] = args.POPUP_PROBABILITY
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['SILENT_NIGHT'] = args.SILENT_NIGHT
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['HIDDEN_MODE'] = args.HIDDEN_MODE
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['SHOW_WELCOME_DIALOG'] = args.SHOW_WELCOME_DIALOG
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['SHOW_FINAL_DIALOG'] = args.SHOW_FINAL_DIALOG
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['FINAL_DIALOG_URL'] = args.FINAL_DIALOG_URL

	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['WAVES'] = create_waves()
	epi_config['dataRequests']['edu.mit.media.funf.probe.builtin.EpidemicProbe'][0]['DAILY_DIGESTS'] = create_daily_digest(summary)
	

	debug(epi_config, "epi config")
	return epi_config

def create_daily_digest(summary):
	return base64.b64encode(json.dumps(summary))

def create_waves():
	waves = {}
	
	#add_wave(waves, start_time='2014-08-09 12:05:00', infected_tag=make_hash('one'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=360, recovered_duration=1080, state_after_infected='R', vaccinated_duration=120, wave_no=1)
	add_wave(waves, start_time='2014-08-12 14:00:00', infected_tag=make_hash('one'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=1)
	add_wave(waves, start_time='2014-08-12 17:00:00', infected_tag=make_hash('two'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=2)
	add_wave(waves, start_time='2014-08-12 20:00:00', infected_tag=make_hash('three'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=3)
	add_wave(waves, start_time='2014-08-12 23:00:00', infected_tag=make_hash('four'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=4)
	
	add_wave(waves, start_time='2014-08-13 09:00:00', infected_tag=make_hash('five'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=5)
	add_wave(waves, start_time='2014-08-13 12:00:00', infected_tag=make_hash('six'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=6)
	add_wave(waves, start_time='2014-08-13 15:00:00', infected_tag=make_hash('seven'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=7)
	add_wave(waves, start_time='2014-08-13 18:00:00', infected_tag=make_hash('eight'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=8)
	
	add_wave(waves, start_time='2014-08-13 21:00:00', infected_tag=make_hash('nine'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=9)
	add_wave(waves, start_time='2014-08-13 23:59:00', infected_tag=make_hash('ten'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=10)
	add_wave(waves, start_time='2014-08-14 09:00:00', infected_tag=make_hash('eleven'), infection_probability=0.0225, starting_state='RA_0.3', exposed_duration=36, recovered_duration=108, state_after_infected='R', vaccinated_duration=120, wave_no=11)
	
	return create_time_series(waves)

def add_wave(waves, start_time, infected_tag, infection_probability, starting_state, exposed_duration, recovered_duration, state_after_infected, vaccinated_duration, wave_no):
	waves[start_time] = '%s,%s,%s,%s,%s,%s,%s,%s'%(infected_tag, infection_probability, starting_state,exposed_duration, recovered_duration, state_after_infected, vaccinated_duration, wave_no)



def make_hash(value,l=8):
	return hashlib.sha1(value).hexdigest()[:l]

def create_time_series(values):
	time_series = []
	for v in sorted(values):
		time_series.append(parser.parse(v).strftime('%s')+'!'+values[v])

	return ';'.join(time_series)

def save_config(config, name):
	f = open(name, 'w')
	f.write(json.dumps(config))
	f.close()
	

if __name__ == "__main__":
	args = build_args()
	debug(args, "args")
	base_config = load_base_config(args.base_config)
	epi_config = create_epi_config(base_config)
	save_config(epi_config)

