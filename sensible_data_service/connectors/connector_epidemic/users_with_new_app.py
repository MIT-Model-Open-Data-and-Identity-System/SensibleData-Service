from utils import db_wrapper
import base64
import json
import os

MIN_VERSION = 1

def users_with_new_app():
	db = db_wrapper.DatabaseHelper()
	last_id = 0
	users = set()
	all_users = set()
	this_path = os.path.split(os.path.realpath(__file__))[0] + '/'

	while True:
		cur = db.retrieve(params={'limit':100000, 'sortby':'timestamp', 'order':1, 'after': last_id}, collection='edu_mit_media_funf_probe_builtin_EpidemicProbe', roles='')
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
