import MySQLdb as mdb
import json
import base64 
import pdb
import sys
from django.conf import settings
from utils import SECURE_settings
from anonymizer.anonymizer import Anonymizer
import datetime

NAME = "facebook_friends_question"

def run():
	conn, cursor = get_cursor()
	#collections = ['main', 'developer', 'researcher']
	collections = ['main','developer', 'researcher']
	for collection in collections:
		ids = get_facebook_ids(cursor, collection)
		edges = build_network(conn.cursor(mdb.cursors.DictCursor), collection, ids)
		update_question_db(conn, conn.cursor(mdb.cursors.DictCursor), collection, edges)
	pass

def get_friends_connections(request, user, scopes, users_to_return, user_roles, own_data):
	collection = 'main'
	if 'researcher' in user_roles: collection = 'researcher'
	elif 'developer' in user_roles: collection = 'developer'

	if len(users_to_return) > 1 or 'all' in users_to_return: return {'error':'This functionality is not yet implemented'}
	conn, cursor = get_cursor()
	friends, connections = get_ego_network(cursor, collection, users_to_return[0])	
        anon = Anonymizer()
	return anon.deanonymizeDocument({'friends':list(friends), 'connections':list(connections)}, 'dk_dtu_compute_facebook_friends')


def myprint(data):
	sys.stdout.write("\r\x1b[K"+data.__str__())
	sys.stdout.flush()

def get_cursor():
	connection = mdb.connect(settings.DATA_DATABASE_SQL["READ_HOST"], SECURE_settings.DATA_DATABASE_SQL["username"], SECURE_settings.DATA_DATABASE_SQL["password"], "question_facebook_friends", ssl=SECURE_settings.DATA_DATABASE_SQL["ssl"], charset="utf8", use_unicode=True)
	cursor = connection.cursor(mdb.cursors.DictCursor)
	return connection, cursor

def deblob(data):
	return json.loads(base64.b64decode(data['data']))

def get_id_facebook_matching(cursor, collection):
	cursor.execute("select user, facebook_id from dk_dtu_compute_facebook." +  collection + " where data_type='friends'")
	mapping = dict()
	dummy = cursor.fetchone()
	while dummy:
		mapping[dummy['facebook_id']] = dummy['user']
		dummy = cursor.fetchone()
	return mapping

def get_facebook_ids(cursor, collection):
	cursor.execute("select distinct facebook_id from dk_dtu_compute_facebook." + collection + " where data_type='friends'")
	ids = set()
	for d in cursor.fetchall():
		ids.add(d['facebook_id'])
	return ids

import datetime
import time
def build_network(cursor, collection, users):
	# only look at last two weeks of data
	timestamp = str(datetime.date.fromtimestamp(time.time()-2*7*24*60*60))
	covered_users = set()
	edges = set()
	#total = cursor.execute("select facebook_id, data from " + collection + " where (data_type='friends') and (timestamp>'2014-04-01') and (timestamp<'2014-04-14')  order by timestamp desc")
	total = cursor.execute("select facebook_id, data from dk_dtu_compute_facebook." + collection + " where (data_type='friends') and (timestamp >= '" + timestamp + "') order by timestamp desc")
	dummy = cursor.fetchone()
	counter = 0 
	while dummy:
		if not counter % 100: myprint(str(counter) + '/' + str(total))
		counter +=1
		if dummy['facebook_id'] in covered_users:
			dummy = cursor.fetchone()
			continue
		else: 
			covered_users.add(dummy['facebook_id'])
		data = deblob(dummy)
		for friend in data:
			if friend['id'] not in users: continue
			edges.add((dummy['facebook_id'], friend['id'], ))
			edges.add((friend['id'], dummy['facebook_id'], ))
			
		dummy = cursor.fetchone()
	return edges

def update_question_db(connection, cursor, collection, edges):
	timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	base = 'insert into question_facebook_friends.' + collection + ' (friend_a, friend_b, timestamp_last_seen) values '
	temp = []
	for edge in edges:
		temp.append("('" + edge[0] + "', '" + edge[1] + "', '" + timenow + "')")
		if len(temp) == 100:
			cursor.execute(base + ', '.join(temp) + " ON DUPLICATE KEY UPDATE timestamp_last_seen='" + timenow + "'")
			temp = []
	if len(temp) > 0:
		query = base + ', '.join(temp) + " ON DUPLICATE KEY UPDATE timestamp_last_seen='" + timenow + "'"
		cursor.execute(query)
	connection.commit()

# returns the list of friends and the connections between friends of a user
def _get_ego_network(cursor, collection, facebook_id):
	cursor.execute("select friend_b from question_facebook_friends." + collection + " where friend_a='" + facebook_id + "'")
	friends = []
	friend_row = cursor.fetchone()
	while friend_row:
		friends.append(friend_row['friend_b'])
		friend_row = cursor.fetchone()
	if not friends: return ([], [], )
	friends_str = '(' + ','.join("'" + f + "'" for f in friends) + ')'
	edges = set()
	query = "select friend_a, friend_b from question_facebook_friends." + collection + " where friend_a in " + friends_str + " and friend_b in " + friends_str
	cursor.execute(query)
	for edge in cursor.fetchall():
		edges.add((edge['friend_a'], edge['friend_b'], ))

	return friends, edges

def get_facebook_id(cursor, collection, user_id):
	cursor.execute("select facebook_id from dk_dtu_compute_facebook." + collection + " where user=%s order by timestamp limit 1", (user_id, ))
	return cursor.fetchone()

def get_ego_network(cursor, collection, user_id):
	fb_id = get_facebook_id(cursor, collection, user_id)
	if not fb_id: return ([],[], )
	return _get_ego_network(cursor, collection, fb_id['facebook_id'])
