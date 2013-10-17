from datetime import timedelta
from utils import database
from bson.code import Code
import json
import time


NAME = 'statistics_question'

COLLECTIONS = ['edu_mit_media_funf_probe_builtin_BluetoothProbe', 'edu_mit_media_funf_probe_builtin_CallLogProbe', 'edu_mit_media_funf_probe_builtin_CellProbe', 'edu_mit_media_funf_probe_builtin_ContactProbe', 'edu_mit_media_funf_probe_builtin_HardwareInfoProbe', 'edu_mit_media_funf_probe_builtin_LocationProbe', 'edu_mit_media_funf_probe_builtin_SMSProbe', 'edu_mit_media_funf_probe_builtin_ScreenProbe', 'edu_mit_media_funf_probe_builtin_TimeOffsetProbe', 'edu_mit_media_funf_probe_builtin_WifiProbe']

def run():
	db = database.Database()
	mapper = Code("""
					function() {
						var key = this.user;
						var value = {
							count: 1,
							timestamp_added: this.timestamp_added
						};
						emit(key, value);
					};
				""")

	reducer = Code("""
	 				function(key, values) {
						var reducedObject = {
							count: 0,
							timestamp_added: 0
						};
						values.forEach( function(value) {
							reducedObject.count += value.count;
							if (reducedObject.timestamp_added < value.timestamp_added) {
								reducedObject.timestamp_added = value.timestamp_added;
							}
						});
						return reducedObject;
					};
				""")


	for collection in COLLECTIONS:
		print collection


		output_collection = NAME+'_'+collection
		min_v = findPreviousMax(db, output_collection)
		max_v = time.time()-5*60
		print min_v, max_v
		if min_v > max_v: continue
		print db.db
		r = db.db[collection].map_reduce(mapper, reducer, out={'reduce':output_collection}, query={'timestamp_added':{'$gt': min_v, '$lt': max_v}})
		db.db[output_collection].ensure_index('timestamp_added')
	return


	return True

def findPreviousMax(db, collection):
	previous_max = 0
	try: previous_max = db.getDocuments({}, collection, from_secondary=False).sort('value.timestamp_added', -1).limit(1)[0]['value']['timestamp_added']
	except IndexError: pass
	return previous_max

def data_stats(request, user, scopes, users_to_return, user_roles, own_data):
	db = database.Database()

	query = {'$query':{}}
	if not 'all' in users_to_return:
		query['$query']['_id'] = {'$in':users_to_return}

	results = {}
	for collection in COLLECTIONS:
		results[collection] = {}
		for x in db.getDocuments(query=query, collection=NAME+'_'+collection, roles=user_roles): 
			results[collection][x['_id']] = int(x['value']['count'])



	return results
