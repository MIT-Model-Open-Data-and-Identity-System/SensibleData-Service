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
# import base64

from pprint import pprint


question_collection = 'question_lasse_fb_network'

def run():
    db = DatabaseHelper()

    collection = 'dk_dtu_compute_facebook_friends'
    question_name = 'fb'

    db.execute_named_query(NAMED_QUERIES['question_lasse_facebook_network_create_table'], None)
        
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
            'where': {'data_type': 'friends'},
            'sortby': 'id',
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
                        week = row['timestamp'].isocalendar()[1]
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

    insert_network(question_name, filtered_network)


#TODO: with three db's this can use DBWrapper.insert instead
def insert_network(question_collection, filtered_network):
    db = DBWrapper()
    question_connection = db.get_write_db_connection_for_probe(question_collection)

    keys = ('user_from', 'user_to', 'week')
    val_strings = []
    parameters = []
    for week, week_network in filtered_network.iteritems():
        for user, friends in week_network.iteritems():
            for friend in friends:
                val_strings.append("("+",".join(["%s" for key in keys])+")")
                parameters.append(user)
                parameters.append(friend)
                parameters.append(week)
    value_string = ','.join(val_strings)

    cur = db.execute_query_on_db("""insert ignore into main ({}) values {}""".format(','.join(keys), value_string), question_connection, parameters)
    question_connection.commit()



def answer(request, user, scopes, users_to_return, user_roles, own_data):
    db = DBWrapper()

    params = {
        'limit': page_size,
        'after': page,
        # 'where': {'data_type': 'feed'},
        'sortby': 'id',
        'order': 1
    }
    # roles_to_use = []
    # if own_data and 'researcher' in user_roles: roles_to_use = ['researcher']
    # if own_data and 'developer' in user_roles: roles_to_use = ['developer']

    # Limit to some users
    if not 'all' in users_to_return:
        params['users'] = users_to_return

    cursor = db.retrieve(params=params, collection=question_collection)

    return [c for c in cursor]



if __name__ == "__main__":
    run()
