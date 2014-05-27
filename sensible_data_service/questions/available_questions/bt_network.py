#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db_access.mysql_wrapper import DBWrapper
from db_access.named_queries import NAMED_QUERIES
from utils.db_wrapper import DatabaseHelper
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from connectors.connector_funf import device_inventory
from connectors.connector_raw.raw_data import processApiCall

from pprint import pprint

question_collection = 'question_lasse_bluetooth_network'


def run():
    
    dbHelper = DatabaseHelper()

    latest_timestamp = 0
    try:
        # Delete the previous 4 days to be sure that late uploads are considered
        print "Removed", dbHelper.execute_named_query(NAMED_QUERIES['question_lasse_bluetooth_network_delete_dates'], (date.today()-timedelta(days=4), date.today())).rowcount
        # dbHelper.execute_named_query(NAMED_QUERIES['question_lasse_bluetooth_network_delete_dates'], (date(2014, 4, 8), date.today())).rowcount
    except Exception, e:
        # print e
        try:
            print "creating table question_lasse_bluetooth_network.main"
            dbHelper.execute_named_query(NAMED_QUERIES['question_lasse_bluetooth_network_create_table'], None)
        except _mysql_exceptions.Warning, e:
            pass
    
    cursor = dbHelper.retrieve(params={
            'limit': 1,
            'after': 0,
            'sortby': 'latest_timestamp',
            'order': -1
        }, collection=question_collection)

    if cursor.rowcount > 0:
        print 'getting latest timestamp',
        row = cursor.fetchone()
        latest_timestamp = row['latest_timestamp']
        print latest_timestamp
    

    cursor = dbHelper.execute_named_query(NAMED_QUERIES['question_lasse_bluetooth_network'], (8, 17, latest_timestamp))
    print cursor.rowcount
    # Code below does the same as the query above

    # db = DBWrapper()
    
    # probe = 'edu_mit_media_funf_probe_builtin_BluetoothProbe'

    # question_connection = db.get_write_db_connection_for_probe('question_lasse')
    # connection = db.get_read_db_connection_for_probe(probe)

    # page=-1
    # page_size = 1000
    # deviceInventory = device_inventory.DeviceInventory()

    # more_pages = True
    # while more_pages:
    #     page += 1

    #     cursor = db.execute_query_on_db("""select 
    #             user as user_from, 
    #             bt_mac as user_to, 
    #             timestamp as date
    #         from main
    #         where 
    #             bt_mac != '-1' and (
    #                 hour(`timestamp`) < %s or 
    #                 hour(`timestamp`) >= %s
    #             )
    #         order by id asc
    #         limit %s, %s
    #         """, connection, (8, 17, page*page_size, page_size))
    #     # print 
    #     # print "Query:"
    #     # print cursor._last_executed
    #     # print
        
    #     more_pages = cursor.rowcount > 0

    #     if more_pages:
    #         rows = []
    #         for row in cursor:
    #             r = dict(row)
    #             # Reduce timestamps to dates instead for better binning
    #             r['date'] = date.fromordinal(r['date'].toordinal())
    #             try:
    #                 r['bt_user'] = deviceInventory.mapBtToUser(row['bt_mac'], row['timestamp'], use_mac_if_empty=False)
    #             except KeyError: 
    #                 r['bt_user'] = ''
    #             rows.append(r)

    #         keys = ('user_from', 'user_to', 'date')
    #         value_string = ",".join(["("+",".join(["%s" for key in keys])+")" for row in rows])
    #         parameters = []
    #         for row in rows:
    #             for key in keys:
    #                 # print row
    #                 parameters.append(row[key])

    #         cur = db.execute_query_on_db("""insert into {0} (user_from, user_to, date) 
    #             values 
    #                 {1} 
    #             on duplicate key update 
    #                 occurrences = occurrences+1""".format(question_name, value_string), question_connection, parameters)
    #         question_connection.commit()

    #     del cursor

#TODO: I need three different databases for this to work with the DBWrapper
def answer(request, user, scopes, users_to_return, user_roles, own_data):
    db = DBWrapper()
    probe_settings = {'scope': 'connector_raw.all_data_researcher',
        'collection': question_collection,
        'default_fields': ['id','user_from','user_to','date','occurrences']}

    params = processApiCall(request, probe_settings, users_to_return)

    # Limit to some users
    # if not 'all' in users_to_return:
    #     params['users'] = users_to_return

    cursor = db.retrieve(params=params, collection=question_collection)

    return [c for c in cursor]


if __name__ == "__main__":
    run()
