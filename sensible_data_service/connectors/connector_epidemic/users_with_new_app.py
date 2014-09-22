from utils import db_wrapper
import base64
import json
import os
import time
import datetime

MIN_VERSION = 1

def users_with_new_app():
	db = db_wrapper.DatabaseHelper()
	users = set()
	all_users = set()
	this_path = os.path.split(os.path.realpath(__file__))[0] + '/'


	START_TIME = 1410040800
	WINDOW = 60 * 60 * 10
	END_TIME = time.mktime(datetime.datetime.now().timetuple())

	jj = 0
	while True:
		last_id = 0
		start_time = START_TIME + jj * WINDOW
		end_time = START_TIME + (jj + 1) * WINDOW
		if start_time > END_TIME: break
		jj += 1

		print start_time, end_time

		while True:
			cur = db.retrieve(params={'limit':100000, 'sortby':'timestamp', 'order':1, 'after': last_id, 'start_date': start_time, 'end_date': end_time}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
			if cur.rowcount == 0: break
			last_id += 1
			print last_id

			for row in cur:
				try:
					user = row['user']
					all_users.add(user)
					data = json.loads(base64.b64decode(row['data']))	
					if data['current_version'] >= MIN_VERSION: users.add(user)
				except: pass


	print 'users with verssion below %s:   %s'%(MIN_VERSION, len(all_users - users))
	print 'users with version at least %s:   %s'%(MIN_VERSION, len(users))
	f = open(this_path+'users_ready_for_infection.json', 'w')	
	f.write(json.dumps(list(users)))
	f.close()
