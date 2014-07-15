from utils import db_wrapper
from datetime import datetime
from datetime import timedelta
from connectors.connector_funf import device_inventory
import calendar
from collections import OrderedDict
from django.db import models
import json
from bson import json_util
from db_access.named_queries import NAMED_QUERIES

#http://raman.imm.dtu.dk:8086/magda/sensible-dtu/connectors/connector_answer/v1/who_did_i_see_question/who_did_i_see_answer/?bearer_token=c9af1c97a08500ba33635cf2568ce1&username=331f9e3859ae7f3c457498d423d29d&time=today&output=json
#http://raman.imm.dtu.dk:8086/magda/sensible-dtu/connectors/connector_answer/v1/who_did_i_see_question/who_did_i_see_answer/?bearer_token=f3b4144993be90bd3e701c716dd1de&time=today

NAME = "who_did_i_see_question"

DB_BLUETOOTH = 'edu_mit_media_funf_probe_builtin_BluetoothProbe'
DB_QUESTION = 'question_who_did_i_see'
collections = ['main', 'developer', 'researcher']
TB_NAME = 'researcher'
TB_SCAN = "last_scan_id"
MIN_TIME = 10 #a user has to see somebody for at least 10 minutes to get his name returned
SCAN_DELTA = 5 # the scans are performed every 5 minutes
TOP = 10 # number ot top users to be retrieved
SCAN_CHUNK = 100000

# Initialize device inventory
INVENTORY = device_inventory.DeviceInventory()
    
def run():
    """Main loop to populate the database."""
    collections = ['researcher', 'main', 'developer']
    for collection in collections:
        last_scan_id = _get_last_scan_id(collection)
        print "Computing ", collection, " collection"
        _compute_who_did_i_see(collection, last_scan_id)  
    return True

def who_did_i_see_answer(request, user, scopes, users_to_return, user_roles, own_data):
    """The response for request who_did_i_see_question. Returns the list of people seen by the user within the requested time."""
    [collection, user, from_date, end_date, output_type] = prepare_to_answer(request, users_to_return, user_roles, user)
    result = {}
    for single_user in user:
        users_list = get_users_list(collection, single_user, from_date, end_date)
        top_unique_users_seen = _get_top_unique_users(users_list)
        result[single_user] = top_unique_users_seen
    return json.dumps(result, default=json_util.default)

def prepare_to_answer(request, users_to_return, user_roles, user):
    parsed_request = parse_request(request)
    if isinstance(parsed_request, dict) or (isinstance(parsed_request, list) and len(parsed_request) != 3):
        return json.dumps(parsed_request)
    [from_date, end_date, output_type] = parsed_request
    
    collection = 'main'
    if 'researcher' in user_roles: collection = 'researcher'
    elif 'developer' in user_roles: collection = 'developer'
    
    if 'all' in users_to_return:
        users_to_return = get_all_users('main')
        
    if isinstance(users_to_return, str):
        users_to_return = [users_to_return]    
    
    return [collection, users_to_return, from_date, end_date, output_type]
    
def get_all_users(collection):
    db = db_wrapper.DatabaseHelper()
    cur = db.execute_named_query(NAMED_QUERIES['get_distinct_users_from_' + collection], ()).fetchall()
    ids = set()
    for d in cur:
        ids.add(d['user'])
    return ids
    
def get_users_list(collection, username, from_date, end_date):
    db = db_wrapper.DatabaseHelper()
    return db.execute_named_query(NAMED_QUERIES['get_user_seen_in_time_' + collection], (username, from_date, end_date, )).fetchall()
    
def _get_last_scan_id(collection):
    """ Get the last scan_id from last_scan_id db"""
    db = db_wrapper.DatabaseHelper()
    return db.execute_named_query(NAMED_QUERIES['get_last_scan_id'], (collection, )).fetchone()['id']
    
def _update_last_scan_id(collection, scan_id):
    db = db_wrapper.DatabaseHelper()
    db.execute_named_query(NAMED_QUERIES['update_last_scan_id'], (scan_id, collection, ))    
    
def _compute_who_did_i_see(collection, scan_id):
    while True:
        print "Calculating from scan_id: ", scan_id
        [scan_list, last_scan_id] = _get_new_scan_chunk(collection, scan_id, SCAN_CHUNK)
        scan_id += SCAN_CHUNK
        if not scan_list:
            break;
        chunk_dict = _perform_computations(scan_list)
        _update_question_db(collection, chunk_dict)
        _update_last_scan_id(collection, last_scan_id)
        
def _get_new_scan_chunk(collection, scan_id, SCAN_CHUNK):
    db = db_wrapper.DatabaseHelper()
    cur = db.execute_named_query(NAMED_QUERIES['get_new_scan_chunk_' + collection], (scan_id, (scan_id + SCAN_CHUNK))).fetchall()
    
    id_list = [row['id'] for row in cur]
    print id_list
    if id_list:
        return [cur, max(id_list)]
    return [cur, 0]
        
def _perform_computations(scan_list):
    start_hour = scan_list[0]['timestamp']
    end_hour = start_hour + timedelta(hours = 1)
    curr_hour = start_hour
    idx = 0
    
    chunk_dict = OrderedDict()
    while idx < len(scan_list):
        hour_dict = {}
        while curr_hour < end_hour and idx < len(scan_list):
            curr_hour = scan_list[idx]['timestamp']
            if(scan_list[idx]['bt_mac'] != -1):
                user_seen = INVENTORY.mapBtToUser(scan_list[idx]['bt_mac'], calendar.timegm(scan_list[idx]['timestamp'].utctimetuple()), False)
                if user_seen != None:
                    if(hour_dict.has_key(scan_list[idx]['user'])): # update the key
                        if(hour_dict[scan_list[idx]['user']].has_key(user_seen)): # add 5 mins
                            hour_dict[scan_list[idx]['user']][user_seen] = hour_dict[scan_list[idx]['user']][user_seen] + SCAN_DELTA
                        else:
                            hour_dict[scan_list[idx]['user']][user_seen] = SCAN_DELTA
                    else: # add a new key
                        hour_dict[scan_list[idx]['user']] = { user_seen : SCAN_DELTA }
            idx+=1
        if hour_dict:
            chunk_dict[start_hour] = hour_dict
        # insert into database after one hour
        start_hour = end_hour
        end_hour = start_hour + timedelta(hours = 1)
    return chunk_dict
    
def _update_question_db(collection, chunk_dict):
    for timestamp in chunk_dict.keys():
        for user in chunk_dict[timestamp]:
            for user_seen in chunk_dict[timestamp][user]:
                time_spent = chunk_dict[timestamp][user][user_seen]
                if time_spent >= MIN_TIME or _meeting_occured(collection, timestamp, user, user_seen):
                    _insert_into_question_db(collection, timestamp, user, user_seen, time_spent)                
    return

def _meeting_occured(collection, hour, user, user_seen):
    # we have the case of 5 min meeting # if it is at the end of the hour - check if we met this person also later, and if yes, then we also add it
    db = db_wrapper.DatabaseHelper()
    if (hour + timedelta(minutes = SCAN_DELTA)).hour == hour.hour: #12:03
        cur = db.execute_named_query(NAMED_QUERIES['get_bt_mac_seen_' + collection], (user, hour - timedelta(minutes = SCAN_DELTA), hour, )).fetchall()
    else: #11:58
        cur = db.execute_named_query(NAMED_QUERIES['get_bt_mac_seen_' + collection], (user, hour, hour + timedelta(minutes = SCAN_DELTA), )).fetchall()
    print cur
    return (cur and user_seen == INVENTORY.mapBtToUser(cur[0]['bt_mac'], calendar.timegm(hour.utctimetuple()), False))
    
def _insert_into_question_db(cur, collection, timestamp, user, user_seen, time_spent):
    db = db_wrapper.DatabaseHelper()
    db.execute_named_query(NAMED_QUERIES['insert_who_did_i_see_' + collection], (user, user_seen, timestamp, time_spent, time_spent, ))
    
def _get_top_unique_users(users_list):
    """Returns trimmed list of users to top 10 users"""
    return sorted(users_list, key=lambda user: user['time'], reverse=True)[:TOP] # get top 10 users
        
def get_today(day):
    """Returns tuple of datetimes for today range"""
    from_date = datetime(day.year, day.month, day.day, 0, 0)
    end_date = from_date + timedelta(days = 1)
    return [from_date, end_date]
    
def get_week(day):
    """Returns tuple of datetimes for last week range"""
    end_date = datetime(day.year, day.month, day.day, 0, 0) + timedelta(days = 1)
    from_date = end_date - timedelta(days = 6)
    return [from_date, end_date]
    
def get_month(day):
    """Returns tuple of datetimes for last month range"""
    end_date = datetime(day.year, day.month, day.day, 0, 0) + timedelta(days = 1)
    from_date = end_date - timedelta(days = 29)
    return [from_date, end_date]
        
def parse_request(request):
    """Returns the parsed request"""
    if 'output' in request.GET:
        output_type = request.GET.get('output', '')
    else:
        output_type = 'json' #json by default
        
    if 'time' in request.GET:
        time = request.GET.get('time', '')
    else:
        return json.dumps({ 'error': 'mising time argument' })

    if 'from_date' in request.GET and 'end_date' in request.GET:
        try:
            from_date = models.DateField().to_python(request.GET['from_date'])
        except:
            return json.dumps({ 'error': 'from_date has the wrong format' })
        try:
            end_date = models.DateField().to_python(request.GET['end_date'])
        except:
            return json.dumps({ 'error': 'end_date has the wrong format' })
    elif time == 'today':
        query_date = datetime.now()
        [from_date, end_date] = get_today(query_date)
    elif time == 'week':
        query_date = datetime.now()
        [from_date, end_date] = get_week(query_date)
    elif time == 'month':
        query_date = datetime.now()
        [from_date, end_date] = get_month(query_date)       
    else:
        return json.dumps({ 'error': 'not implemented yet' })

    return [from_date, end_date, output_type]