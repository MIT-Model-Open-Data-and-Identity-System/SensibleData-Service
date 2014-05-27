#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db_access.mysql_wrapper import DBWrapper
from db_access.named_queries import NAMED_QUERIES
from utils.db_wrapper import DatabaseHelper
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from connectors.connector_funf import device_inventory
import json
from collections import defaultdict
import _mysql_exceptions
import bson.json_util as json
from connectors.connector_raw.raw_data import processApiCall
from bt_network import _auth
from django.http import HttpResponse
from sensible_audit import audit

from pprint import pprint

log = audit.getLogger(__name__)

#TODO: Add timestamp row to fb tables

question_collection = 'question_lasse_fb_network'

def run():
    db = DatabaseHelper()

    collection = 'dk_dtu_compute_facebook_friends'
    
    latest_timestamp = 0

    try:
        cursor = dbHelper.retrieve(params={
                'limit': 1,
                'after': 0,
                'sortby': 'timestamp',
                'order': -1
            }, collection=question_collection)
        
        if cursor.rowcount > 0:
            print 'getting latest timestamp'
            row = cursor.fetchone()
            latest_timestamp = row['timestamp']
    except Exception, e:
        try:
            db.execute_named_query(NAMED_QUERIES['question_lasse_fb_network_create_table'], None)
        except _mysql_exceptions.Warning, e:
            pass
    
    # Look at the either the last 4 days or since previous update
    if latest_timestamp and latest_timestamp <= datetime.today() - timedelta(days=4):
        start_date = latest_timestamp - timedelta(days=1)
    else:
        start_date = datetime.today() - timedelta(days=4)

    page=-1
    page_size = 10000

    more_pages = True

    network = defaultdict(lambda: defaultdict(lambda: set()))
    fb_id_to_user = {}

    while more_pages:
        page += 1

        # TODO: Build the whole network first, remove non-study nodes after

        cursor = db.retrieve(params={
            'limit': page_size,
            'after': page,
            'start_date': time.mktime(start_date.timetuple()),
            'where': {'data_type': 'friends'},
            'sortby': 'timestamp',
            'order': 1
        }, collection=collection)
        # print 
        # print "Query:"
        # print cursor._last_executed
        # print

        more_pages = cursor.rowcount > 0

        if more_pages:
            for row in cursor:
              fb_id_to_user[row['facebook_id']] = row['user']
            
            for row in cursor:
                # print row
                # friends = json.loads(row['data'].decode('base64'))
                friends = row['data']
                for friend in friends:
                    if 'id' in friend:
                        week = row['timestamp'] - timedelta(days=row['timestamp'].weekday())
                        week = week.replace(hour=0, minute=0, second=0, microsecond=0)
                        # week = row['timestamp'].isocalendar()[1]
                        if not isinstance(week, (datetime, date, time)):
                            print "weird week", week
                        network[week][row['user']].add(friend['id'])
                # print row['data']
        del cursor

    filtered_network = defaultdict(lambda: defaultdict(lambda: set()))
    for week, week_network in network.iteritems():
        for user, fb_friends in week_network.iteritems():
            for friend in fb_friends:
                if friend in fb_id_to_user:
                    # using min/max to only store each connection once
                    filtered_network[week][min(user, fb_id_to_user[friend])].add(max(user, fb_id_to_user[friend]))
    del network

    # pprint(dict(filtered_network))

    insert_network(question_collection, filtered_network)


#TODO: with three db's this can use DBWrapper.insert instead
def insert_network(collection, filtered_network):
    print "inserting network to", collection
    db = DBWrapper()

    documents = []
    for week, week_network in filtered_network.iteritems():
        for user, friends in week_network.iteritems():
            for friend in friends:
                documents.append({'user_from': user, 'user_to': friend, 'week': week.isocalendar()[1], 'timestamp': week})

    if documents:
        db.insert(documents, collection)

    # db = DBWrapper()
    # question_connection = db.get_write_db_connection_for_probe(collection)

    # keys = ('user_from', 'user_to', 'week')
    # val_strings = []
    # parameters = []
    # for week, week_network in filtered_network.iteritems():
    #     for user, friends in week_network.iteritems():
    #         for friend in friends:
    #             val_strings.append("("+",".join(["%s" for key in keys])+")")
    #             parameters.append(user)
    #             parameters.append(friend)
    #             parameters.append(week)
    # value_string = ','.join(val_strings)

    # cur = db.execute_query_on_db("""insert ignore into main ({}) values {}""".format(','.join(keys), value_string), question_connection, parameters)
    # question_connection.commit()



def answer(request, user, scopes, users_to_return, user_roles, own_data):
    auth = _auth(request)
    if auth == True:
        db = DatabaseHelper()

        probe_settings = {'scope': 'connector_raw.all_data_researcher',
            'collection': question_collection,
            'default_fields': ['id','user_from','user_to','week']}

        params = processApiCall(request, probe_settings, users_to_return)
        

        # Limit to some users
        # if not 'all' in users_to_return:
        #     params['users'] = users_to_return

        cursor = db.retrieve(params=params, collection=question_collection)

        return HttpResponse(json.dumps([c for c in cursor]), content_type="application/json")
    else:
        return auth



if __name__ == "__main__":
    run()
