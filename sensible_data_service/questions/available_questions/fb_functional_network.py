#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from db_access.mysql_wrapper import DBWrapper
from db_access.named_queries import NAMED_QUERIES
from utils.db_wrapper import DatabaseHelper
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from connectors.connector_funf import device_inventory
import json
from collections import defaultdict
from fb_network import insert_network
import _mysql_exceptions
# import base64
from pprint import pprint


question_collection = 'question_lasse_facebook_functional_network'


def run():
    db = DatabaseHelper()

    collection = 'dk_dtu_compute_facebook_feed'

    try:
        print NAMED_QUERIES['question_lasse_facebook_functional_network_create_table']
        c = db.execute_named_query(NAMED_QUERIES['question_lasse_facebook_functional_network_create_table'], None)
    except _mysql_exceptions.Warning, e:
        print e
        pass
       
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
            'where': {'data_type': 'feed'},
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
                # print row['data']
                # wall = json.loads(row['data'].decode('base64'))
                wall = row['data']
                # pprint(wall)
                for status in wall.itervalues():
                    # story_tags is deprecated, but some data in the db are captured from before
                    for tag_type in ('story_tags', 'message_tags'): 
                        if tag_type in status:
                            # For some reason this is a nested dict with only one entry
                            for temp in status[tag_type].values():
                                for tag in temp.values():
                                    # If right kind of tag and the tag is not the user itself (often is)
                                    if 'type' in tag and tag['type']=='user' and 'id' in tag and not row['facebook_id'] == tag['id']:
                                        week = row['timestamp'] - timedelta(days=row['timestamp'].weekday())
                                        week = week.replace(hour=0, minute=0, second=0, microsecond=0)
                                        network[week][row['user']].add(tag['id'])
            
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



def answer(request, user, scopes, users_to_return, user_roles, own_data):
    db = DBWrapper()

    probe_settings = {'scope': 'connector_raw.all_data_researcher',
        'collection': question_collection,
        'default_fields': ['id','user_from','user_to','week']}

    params = processApiCall(request, probe_settings, users_to_return)
    
    # Limit to some users
    # if not 'all' in users_to_return:
    #     params['users'] = users_to_return

    cursor = db.retrieve(params=params, collection=question_collection)

    return [c for c in cursor]


if __name__ == "__main__":
    run()
