from datetime import timedelta
from utils import database
from bson.code import Code
import json
import time


NAME = 'daily_statistics_question'

COLLECTIONS = ['edu_mit_media_funf_probe_builtin_BluetoothProbe', 'edu_mit_media_funf_probe_builtin_CallLogProbe', 'edu_mit_media_funf_probe_builtin_CellProbe', 'edu_mit_media_funf_probe_builtin_ContactProbe', 'edu_mit_media_funf_probe_builtin_HardwareInfoProbe', 'edu_mit_media_funf_probe_builtin_LocationProbe', 'edu_mit_media_funf_probe_builtin_SMSProbe', 'edu_mit_media_funf_probe_builtin_ScreenProbe', 'edu_mit_media_funf_probe_builtin_TimeOffsetProbe', 'edu_mit_media_funf_probe_builtin_WifiProbe']

def run():
	db = database.Database()
	mapper = Code("""
					function() {
						var date = new Date(this.data.TIMESTAMP*1000);
						var month = ('0'+(date.getMonth()+1)).substr(-2);
						var day = ('0'+date.getDate()).substr(-2);
						var dateString = date.getFullYear() + '-' + month + '-' + day;
						var key = this.user + '_' + dateString; 
						var dayCount = 0;
						if (date.getHours() > 1) dayCount = 1;
						var value = {
							user: this.user,
							date: dateString,
							count: 1,
							day_count: dayCount,
							timestamp_added: this.timestamp_added
						};
						emit(key, value);
					};
				""")

	reducer = Code("""
	 				function(key, values) {
						var reducedObject = {
							user: key.split('_')[0],
							date: key.split('_')[1],
							count: 0,
							day_count: 0,
							timestamp_added: 0
						};
						values.forEach( function(value) {
							reducedObject.count += value.count;
							reducedObject.day_count += value.day_count;
							if (reducedObject.timestamp_added < value.timestamp_added) {
								reducedObject.timestamp_added = value.timestamp_added;
							}
						});
						return reducedObject;
					};
				""")


	for collection in COLLECTIONS:
		print "%s %s"%(NAME, collection)


		output_collection = NAME+'_'+collection
		min_v = findPreviousMax(db, output_collection)
		max_v = time.time()-5*60
		print min_v, max_v
		if min_v > max_v: continue
		r = (db.getDatabase(collection))[collection].map_reduce(mapper, reducer, out={'reduce':output_collection}, query={'timestamp_added':{'$gt': min_v, '$lt': max_v}})
		(db.getDatabase(output_collection))[output_collection].ensure_index('timestamp_added')
	return


	return True

def findPreviousMax(db, collection):
	previous_max = 0
	try: previous_max = db.getDocuments({}, collection, from_secondary=False).sort('value.timestamp_added', -1).limit(1)[0]['value']['timestamp_added']
	except IndexError: pass
	return previous_max

def daily_data_stats(request, user, scopes, users_to_return, user_roles, own_data):
	db = database.Database()

	roles_to_use = []
	if own_data and 'researcher' in user_roles: roles_to_use = ['researcher']
	if own_data and 'developer' in user_roles: roles_to_use = ['developer']


	collections_to_use = request.GET.get('collections','')
	if collections_to_use == '': collections_to_use = [x for x in COLLECTIONS]
	else: collections_to_use = collections_to_use.split(',')

	collections_to_use = [x for x in set(collections_to_use).intersection(set(COLLECTIONS))]

	query = {'$query':{}}
	if not 'all' in users_to_return:
		query['$query']['value.user'] = {'$in':users_to_return}

	results = {}
	for collection in collections_to_use:
		results[collection] = {}
		for x in db.getDocuments(query=query, collection=NAME+'_'+collection, roles=roles_to_use): 
			try: results[collection][x['value']['user']][x['value']['date']] = int(x['value']['count'])
			except KeyError: 
				results[collection][x['value']['user']] = {}
				results[collection][x['value']['user']][x['value']['date']] = int(x['value']['count'])



	return results
