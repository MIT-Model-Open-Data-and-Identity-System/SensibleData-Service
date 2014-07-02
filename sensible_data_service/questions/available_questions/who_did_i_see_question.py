import MySQLdb as mdb
from utils import SECURE_settings
from sensible_data_service import LOCAL_SETTINGS
from datetime import datetime
from datetime import timedelta
from connectors.connector_funf import device_inventory
import calendar
from collections import OrderedDict
from django.db import models

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
    db_data = connect_to_db_data()
    db_question = connect_to_db_question()
    collections = ['researcher', 'main', 'developer']
    for collection in collections:
        last_scan_id = _get_last_scan_id(db_question, collection)
        print "Computing ", collection, " collection"
        _compute_who_did_i_see(db_data, db_question, collection, last_scan_id)  
    db_data.close()
    db_question.close()
    return True

def who_did_i_see_answer(request, user, scopes, users_to_return, user_roles, own_data):
    """The response for request who_did_i_see_question. Returns the list of people seen by the user within the requested time."""
    [db_connection, collection, user, from_date, end_date, output_type] = prepare_to_answer(request, user_roles, user)
    users_list = get_users_list(db_connection, collection, user, from_date, end_date)
    top_unique_users_seen = _get_top_unique_users(users_list)
    return prepare_answer(output_type, top_unique_users_seen)

def prepare_to_answer(request, user_roles, user):
    parsed_request = parse_request(request)
    if isinstance(parsed_request, dict) or (isinstance(parsed_request, list) and len(parsed_request) != 3):
        return prepare_answer(parsed_request)
    [from_date, end_date, output_type] = parsed_request
    db_connection = connect_to_db_question()
    
    collection = 'main'
    if 'researcher' in user_roles: collection = 'researcher'
    elif 'developer' in user_roles: collection = 'developer'
    
    #if len(users_to_return) > 1 or 'all' in users_to_return: 
    #    return {'error':'This functionality is not yet implemented'}
    
    user = '0010fedde8e61cad5b049da6df8b5a'
    return [db_connection, collection, user, from_date, end_date, output_type]
    
def get_users_list(db, collection, username, from_date, end_date):
    cur = db.cursor()
    cur.execute("SELECT user_seen, time, timestamp FROM " + collection + " WHERE user = %s AND timestamp BETWEEN %s AND %s", (username, from_date, end_date))
    result = cur.fetchall()
    cur.close()
    return result
    
def _get_last_scan_id(db, collection):
    """ Get the last scan_id from last_scan_id db"""
    cur = db.cursor()
    query = "SELECT id FROM last_scan_id WHERE table_name = %s"
    cur.execute(query, (collection))
    result = cur.fetchall()
    cur.close()
    return result[0]['id']
    
def _update_last_scan_id(db, collection, scan_id):
    cur = db.cursor()
    query = 'UPDATE last_scan_id SET id = %s WHERE table_name = %%s' % (scan_id)
    cur.execute(query, (collection))
    db.commit()
    cur.close()
    
def _compute_who_did_i_see(db_data, db_question, collection, scan_id):
    while True:
        print "Calculating from scan_id: ", scan_id
        [scan_list, last_scan_id] = _get_new_scan_chunk(db_data, collection, scan_id, SCAN_CHUNK)
        scan_id += SCAN_CHUNK
        if not scan_list:
            break;
        chunk_dict = _perform_computations(db_question, scan_list)
        _update_question_db(db_data, db_question, collection, chunk_dict)
        _update_last_scan_id(db_question, collection, last_scan_id)
        
def _get_new_scan_chunk(db, collection, scan_id, SCAN_CHUNK):
    cur = db.cursor()
    query = 'SELECT id, user, bt_mac, timestamp FROM %s WHERE id > %s AND id < %s ORDER BY timestamp' % (collection, scan_id, (scan_id + SCAN_CHUNK))
    cur.execute(query)
    fetched_data = cur.fetchall()
    cur.close()
    
    id_list = [row['id'] for row in fetched_data]
    if id_list:
        return [fetched_data, max(id_list)]
    return [fetched_data, 0]
        
def _perform_computations(db_question, scan_list):
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
    
def _update_question_db(db_data, db_question, collection, chunk_dict):
    cur = db_question.cursor()
    for timestamp in chunk_dict.keys():
        for user in chunk_dict[timestamp]:
            for user_seen in chunk_dict[timestamp][user]:
                time_spent = chunk_dict[timestamp][user][user_seen]
                if time_spent >= MIN_TIME or _meeting_occured(db_data, collection, timestamp, user, user_seen):
                    _insert_into_question_db(cur, collection, timestamp, user, user_seen, time_spent)                
    db_question.commit()
    cur.close()
    return

def _meeting_occured(db_data, collection, hour, user, user_seen):
    # we have the case of 5 min meeting # if it is at the end of the hour - check if we met this person also later, and if yes, then we also add it
    cur = db_data.cursor()
    query = "SELECT bt_mac FROM %s WHERE user = %%s AND timestamp BETWEEN %%s AND %%s" % collection
    if (hour + timedelta(minutes = SCAN_DELTA)).hour == hour.hour: #12:03
        cur.execute(query, (user, hour - timedelta(minutes = SCAN_DELTA), hour))
    else: #11:58
        cur.execute(query, (user, hour, hour + timedelta(minutes = SCAN_DELTA)))
    fetched_data = cur.fetchall()
    return (fetched_data and user_seen == INVENTORY.mapBtToUser(fetched_data[0]['bt_mac'], calendar.timegm(hour.utctimetuple()), False))
    
def _insert_into_question_db(cur, collection, timestamp, user, user_seen, time_spent):
    query = "INSERT INTO %s (user, user_seen, timestamp, time) " % collection
    query = query + "VALUES (%s, %s, %s, %s) "
    query = query + "ON DUPLICATE KEY UPDATE time = time + %s"
    cur.execute(query, (user, user_seen, timestamp, time_spent, time_spent))
    
def _get_top_unique_users(users_list):
    """Returns trimmed list of users to top 10 users"""
    return sorted(users_list, key=lambda user: user['time'], reverse=True)[:TOP] # get top 10 users
    
def prepare_answer(output_type, answer):
    #TODO: fix CSV output
    """Returns the result in appropriate type according to output_type variable"""
    if output_type == 'json':
        return str(answer)
    elif output_type == 'csv':
        if isinstance(answer, dict) or isinstance(answer, list):
            result = ''
            for item in answer:
                if isinstance(item, tuple) and len(item) == 2:
                    result += str(item[0]) + ', ' + str(item[1]) + ', '
                else:
                    result += str(item['user_seen']) + ', ' + str(item['time']) + ', '
            return str(result)
        else:
            return { str(result): ' not supported format' }
    else:
        return { 'error': 'not implemented yet' }
        
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
    
def connect_to_db_data():
    """Returns valid connestion to the database"""
    try:
        db_data = mdb.connect(host = LOCAL_SETTINGS.DATA_DATABASE_REMOTE['HOST'], user = SECURE_settings.DATA_DATABASE_BIG_SQL['username'], passwd = SECURE_settings.DATA_DATABASE_BIG_SQL['password'], db = DB_BLUETOOTH, cursorclass=mdb.cursors.DictCursor)
        return db_data
    except mdb.Error, err:
        raise err
        
def connect_to_db_question():
    """Returns valid connestion to the database"""
    try:
        db_data = mdb.connect(host = LOCAL_SETTINGS.DATA_QUESTION_DATABASE['HOST'], user = SECURE_settings.DATA_DATABASE_SQL['username'], passwd = SECURE_settings.DATA_DATABASE_SQL['password'], db = DB_QUESTION, cursorclass=mdb.cursors.DictCursor)
        return db_data
    except mdb.Error, err:
        raise err
        
def parse_request(request):
    # TODO: Cross side scripting?
    """Returns the parsed request"""
    if 'output' in request.GET:
        output_type = request.GET.get('output', '')
    else:
        output_type = 'json' #json by default
        
    if 'time' in request.GET:
        time = request.GET.get('time', '')
    else:
        return prepare_answer(output_type, { 'error': 'mising time argument' })

    if 'from_date' in request.GET and 'end_date' in request.GET:
        try:
            from_date = models.DateField().to_python(request.GET['from_date'])
        except:
            return prepare_answer(output_type, { 'error': 'from_date has the wrong format' })
        try:
            end_date = models.DateField().to_python(request.GET['end_date'])
        except:
            return prepare_answer(output_type, { 'error': 'end_date has the wrong format' })
    elif time == 'today':
        query_date = datetime.now()
        query_date = datetime(2014,01,06)
        [from_date, end_date] = get_today(query_date)
    elif time == 'week':
        query_date = datetime.now()
        query_date = datetime(2014,01,06)
        [from_date, end_date] = get_week(query_date)
    elif time == 'month':
        query_date = datetime.now()
        query_date = datetime(2014,01,06)
        [from_date, end_date] = get_month(query_date)       
    else:
        return prepare_answer(output_type, { 'error': 'not implemented yet' })

    return [from_date, end_date, output_type]