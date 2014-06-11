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

NAME = "who_did_i_see_question"

DB_BLUETOOTH = 'edu_mit_media_funf_probe_builtin_BluetoothProbe'
DB_QUESTION = 'question_who_did_i_see'
TB_DATA = 'researcher'
MIN_TIME = 10 #a user has to see somebody for at least 10 minutes to get his name returned
SCAN_DELTA = 5 # the scans are performed every 5 minutes
TOP = 10 # number ot top users to be retrieved

# Initialize device inventory
INVENTORY = device_inventory.DeviceInventory()

def run():
    """Main loop to populate the database."""
    pass

def who_did_i_see_answer(request, user, scopes, users_to_return, user_roles, own_data):
    """The response for request who_did_i_see_question. Returns the list of people seen by the user within the requested time."""
    parsed_request = parse_request(request)
    if isinstance(parsed_request, dict) or (isinstance(parsed_request, list) and len(parsed_request) != 4):
        return parsed_request
    [username, from_date, end_date, output_type] = parsed_request
    db_connection = connect_to_db()

    users_list = get_users_list(db_connection, username, from_date, end_date)
    users_seen = _get_met_users(users_list, SCAN_DELTA)
    top_unique_users_seen = _get_top_unique_users(users_seen)
    return prepare_answer(output_type, top_unique_users_seen)

def parse_request(request):
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
        #query_date = datetime.now
        query_date = datetime(2014, 1, 16)
        [from_date, end_date] = get_today(query_date)
    elif time == 'week':
        #query_date = datetime.now
        query_date = datetime(2014, 1, 16)
        [from_date, end_date] = get_week(query_date)
    else:
        return prepare_answer(output_type, { 'error': 'not implemented yet' })

    if 'username' in request.GET:
        username = request.GET.get('username', '')
    else:
        return prepare_answer(output_type, { 'error': 'missing username argument' }) # ask about getting username from token etc.
    return [username, from_date, end_date, output_type]
    
def connect_to_db():
    """Returns valid connestion to the database"""
    try:
        db_data = mdb.connect(host = LOCAL_SETTINGS.DATA_QUALITY_DATABASE['HOST'], user = SECURE_settings.DATA_DATABASE_SQL['username'], passwd = SECURE_settings.DATA_DATABASE_SQL['password'], db = DB_BLUETOOTH, cursorclass=mdb.cursors.DictCursor)
        return db_data
    except mdb.Error, err:
        raise err
    
def get_users_list(db, user_id, start, end):
    """Returns the list of users that have been seen by the user within a given time"""
    #execute query
    cur = db.cursor()
    query = 'SELECT bt_mac, timestamp FROM %s WHERE user = %%s  AND timestamp BETWEEN %%s AND %%s ORDER BY bt_mac' % (TB_DATA)
    try:
        cur.execute(query, (user_id, start, end))
        fetched_data = cur.fetchall()
        cur.close()
    except:
        return { 'error': 'bad query' }

    # compute usernames from bt_macs
    bt_mac_list = [(bt_mac['bt_mac'], bt_mac['timestamp']) for bt_mac in fetched_data]
    return _get_users_from_macs(bt_mac_list)

def _get_met_users(users_timestamp_list, delta):
    """Returns the list of users that were seen for >= 10 mins"""
    users_seen = OrderedDict()
    unique_users_list = [item[0] for item in list(OrderedDict.fromkeys(users_timestamp_list))]
    users_list = [item[0] for item in users_timestamp_list]
    for user in unique_users_list:
        if(users_list.count(user) >= round(MIN_TIME / delta)):
            users_seen[user] = users_list.count(user) * delta
    return users_seen

def _get_top_unique_users(users_list):
    """Returns trimmed list of users to top 10 users"""
    return sorted(users_list.items(), key=lambda user: user[1], reverse=True)[:TOP] # get top 10 users

def _get_users_from_macs(bt_mac_list):
    """Returns usernames mapped from bt_mac list"""
    users_timestamp_list = []
    for bt_mac in bt_mac_list:
        if bt_mac[0] != '-1':
            username = ''
            username = INVENTORY.mapBtToUser(bt_mac[0], calendar.timegm(bt_mac[1].utctimetuple()), False)
            if username != None:
                users_timestamp_list.append((username, bt_mac[1]) )
    return users_timestamp_list
    
def prepare_answer(output_type, answer):
    """Returns the result in appropriate type according to output_type variable"""
    if output_type == 'json':
        if isinstance(answer, dict):
            return answer
        elif isinstance(answer, list):
            result = OrderedDict()
            for item in answer:
                if isinstance(item, tuple):
                    result[str(item[0])] = str(item[1])
            return result
        else:
            return { str(result): ' not supported format' }
    elif output_type == 'csv':
        if isinstance(answer, dict):
            result = ''
            for item in answer.items():
                if isinstance(item, tuple) and len(item) == 2:
                    result += str(item[0]) + ', ' + str(item[1]) + ', '
                else:
                    result += str(item.key) + ', ' + str(item.value) + ', '
            return result
        elif isinstance(answer, list):
            result = ''
            for item in answer:
                if isinstance(item, tuple) and len(item) == 2:
                    result += str(item[0]) + ', ' + str(item[1]) + ', '
                else:
                    result += str(item) + ', '
            return result
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
    