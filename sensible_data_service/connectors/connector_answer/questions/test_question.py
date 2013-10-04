from datetime import timedelta
from utils import database
from bson.code import Code
import json
import time

NAME = 'test_question'
SCHEDULE = { 'schedule': timedelta(seconds=30), 'args': (16, 16) }

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



	collection = 'edu_mit_media_funf_probe_builtin_BluetoothProbe_researcher'
	output_collection = NAME
	
	min_v = findPreviousMax(db, output_collection)
	max_v = time.time()-5*60
	if min_v > max_v: return False

	r = db.db[collection].map_reduce(mapper, reducer, out={'reduce':output_collection}, query={'timestamp_added':{'$gt': min_v, '$lt': max_v}})
	db.db[output_collection].ensure_index('value.timestamp_added', 1)

	return True

def findPreviousMax(db, collection):
	previous_max = 0
	try: previous_max = db.getDocuments({}, collection).sort('value.timestamp_added', -1).limit(1)[0]['value']['timestamp_added']
	except IndexError: pass
	return previous_max
