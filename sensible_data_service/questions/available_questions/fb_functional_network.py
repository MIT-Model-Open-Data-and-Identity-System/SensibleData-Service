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
import bson.json_util as json
from connectors.connector_raw.raw_data import processApiCall
from django.http import HttpResponse
from sensible_audit import audit

from pprint import pprint


log = audit.getLogger(__name__)

question_collection = 'question_lasse_fb_functional_network'


def run():
    db = DatabaseHelper()

    collection = 'dk_dtu_compute_facebook_feed'
    latest_timestamp = 0

    try:
        # Getting latest timestamp
        cursor = db.retrieve(params={
                'limit': 1,
                'after': 0,
                'sortby': 'timestamp',
                'order': -1
            }, collection=question_collection)
        
        if cursor.rowcount > 0:
            row = cursor.fetchone()
            latest_timestamp = row['timestamp']
    except Exception, e:
        log.error({'type': 'question_lasse', 'tag': 'fb_func_latest_timestamp', 'exception': str(e)})
    
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
            'where': {'data_type': 'feed'},
            'sortby': 'timestamp',
            'order': 1
        }, collection=collection)


        more_pages = cursor.rowcount > 0

        if more_pages:
            for row in cursor:
                fb_id_to_user[row['facebook_id']] = row['user']
            
            for row in cursor:
                # wall = json.loads(row['data'].decode('base64'))
                wall = row['data']
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
    # collection = 'main'
    # if 'researcher' in user_roles: collection = 'researcher'
    # elif 'developer' in user_roles: collection = 'developer'

    db = DatabaseHelper()

    probe_settings = {'scope': 'connector_raw.all_data_researcher',
        'collection': question_collection,
        'default_fields': ['id','user_from','user_to','week']}

    params = processApiCall(request, probe_settings, users_to_return)

    # Limit to some users
    # if not 'all' in users_to_return:
    #     params['users'] = users_to_return

    cursor = db.retrieve(params=params, collection=question_collection, roles=user_roles)

    return HttpResponse(json.dumps([c for c in cursor]), content_type="application/json")
    

if __name__ == "__main__":
    run()
