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
from authorization_manager import authorization_manager
import bson.json_util as json
from django.http import HttpResponse
from sensible_audit import audit

from pprint import pprint

question_collection = 'question_lasse_bluetooth_network'

log = audit.getLogger(__name__)

def run():
    
    dbHelper = DatabaseHelper()

    latest_timestamp = 0
    try:
        # Delete the previous 4 days to be sure that late uploads are considered
        dbHelper.execute_named_query(NAMED_QUERIES['question_lasse_bluetooth_network_delete_dates'], (date.today()-timedelta(days=4), date.today()))
    except Exception, e:
        log.error({'type': 'question_lasse', 'tag': 'bt_delete_prev', 'exception': str(e)})
    
    # getting latest timestamp
    try:
        cursor = dbHelper.retrieve(params={
                'limit': 1,
                'after': 0,
                'sortby': 'latest_timestamp',
                'order': -1
            }, collection=question_collection)

        if cursor.rowcount > 0:
            row = cursor.fetchone()
            latest_timestamp = row['latest_timestamp']
    except Exception, e:
        log.error({'type': 'question_lasse', 'tag': 'bt_latest_timestamp', 'exception': str(e)})
    

    cursor = dbHelper.execute_named_query(NAMED_QUERIES['question_lasse_bluetooth_network'], (8, 17, latest_timestamp))
   


def answer(request, user, scopes, users_to_return, user_roles, own_data):
    

    db = DatabaseHelper()
    probe_settings = {'scope': 'connector_raw.all_data_researcher',
        'collection': question_collection,
        'default_fields': ['id','user_from','user_to','timestamp','occurrences']}

    params = processApiCall(request, probe_settings, users_to_return)

    # Limit to some users
    # if not 'all' in users_to_return:
    #     params['users'] = users_to_return

    cursor = db.retrieve(params=params, collection=question_collection, roles=user_roles)

    return HttpResponse(json.dumps([c for c in cursor]), content_type="application/json")


if __name__ == "__main__":
    run()
