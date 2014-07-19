"""
The bluetooth discoverability question computes the discoverability of bluetooth devices of SensibleDTU users.

In order to run the question, start django shell and then type following commands:

>>> from questions import tasks
>>> run("bluetooth_disc_question") 

Author: Magdalena Furman s110848
"""


from datetime import datetime
from datetime import timedelta
import MySQLdb
from connectors.connector_funf import device_inventory
import calendar
from sensible_data_service import LOCAL_SETTINGS
from utils import SECURE_settings
import json

# Name of the question
NAME = 'bluetooth_disc_question'

# Quality settings
DELTA = 7 # number of days during which we dont assign the user as undiscoverable
ITER = 100000 # fraction of data that has to be calculated in one iteration

COLLECTIONS = {'edu_mit_media_funf_probe_builtin_BluetoothProbe' : 'bluetooth'}

TB_BLUETOOTH_DAILY = 'bluetooth_disc_daily'

DB_QUALITY = 'data_quality'
DB_DATA = 'main'

DAYS = 50 # number of days to export the data to file

# Initialize device inventory
device_inventory = device_inventory.DeviceInventory()

def run():
    """Main loop of data quality question. """
    print "Executing ", NAME
    try:
        db_quality = MySQLdb.connect(host = LOCAL_SETTINGS.DATA_QUALITY_DATABASE['HOST'], user = SECURE_settings.DATA_DATABASE_SQL['username'], passwd = SECURE_settings.DATA_DATABASE_SQL['password'], db = DB_QUALITY)
        print 'Connected to database: ', DB_QUALITY
    except MySQLdb.Error, err:
        print "Error %d: %s" % (err.args[0], err.args[1])

    for connection in COLLECTIONS.keys():
        try:
            db_data = MySQLdb.connect(host = LOCAL_SETTINGS.DATA_DATABASE_REMOTE['HOST'], user = SECURE_settings.DATA_DATABASE_BIG_SQL['username'], passwd = SECURE_settings.DATA_DATABASE_BIG_SQL['password'], db = connection)
            print 'Connected to database: ', connection
        except MySQLdb.Error, err:
            print "Error %d: %s" % (err.args[0], err.args[1])
            break
        
        [users_prob, users_day] = prepare_users_prob(db_data)
        calc_bdisc(db_data, db_quality, users_prob, users_day)
        print "po liczeniu"
        get_last_month_disc(db_quality, DAYS)
        
        db_data.close()
    db_quality.close()

def get_data_stats(request, days=30, output_type="tsv"):
    """Get the bluetooth discoverability for all users uring last X days.

    Keyword arguments:
    request -- url request
    days -- number of days to fetch data
    output_type -- type of output file, 'json' or 'tsv'

    """
    try:
        db_quality = MySQLdb.connect(host = LOCAL_SETTINGS.DATA_QUALITY_DATABASE['HOST'], user = SECURE_settings.DATA_DATABASE_SQL['username'], passwd = SECURE_settings.DATA_DATABASE_SQL['password'], db = DB_QUALITY)
        print 'Connected to database: ', DB_QUALITY
    except MySQLdb.Error, err:
        print "Error %d: %s" % (err.args[0], err.args[1])
        
    if output_type == "json":
        results = {}
    elif output_type == "tsv":
        results = "username\tall\tmonth\tweek\n"

        cur = db_quality.cursor()
        query = 'SELECT bt_mac, start_timestamp, value FROM %s WHERE start_timestamp > DATE_SUB(%%s, INTERVAL %s DAY)' % (TB_BLUETOOTH_DAILY, days)
        cur.execute(query)
        result = cur.fetchall()
        cur.close()

        for row in result:
            if output_type == "json":
                if results.has_key(row[0]):
                    results[row[0]][row[1]] = row[2]
                else:
                    results[row[0]] = {"date" : row[1], "value" : row[2]}
            elif output_type == "tsv":
                results = results + row[0] + "\t" + datetime.strftime(row[1], "%Y%m%d") + "\t" + str(row[2]) + "\n"

    if output_type == "json":
        return json.dumps(results)
    elif output_type == "tsv":
        return results
    else:
        return ""
        
def get_last_bluetooth_disc_scan_id(db):
    """ Get the last scan_id from bluetooth_last_scan table processed data"""
    cur = db.cursor()
    query = "SELECT scan_id FROM bluetooth_last_scan"
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result[0][0]
    
def insert_into_disc(db, table_name, bt_mac, start_timestamp, end_timestamp, value):
    cur = db.cursor()
    query = 'INSERT INTO %s (bt_mac, start_timestamp, end_timestamp, value) ' % table_name
    query = query + 'VALUES (%s, %s, %s, %s) '
    query = query + 'ON DUPLICATE KEY UPDATE value = %s'
    cur.execute(query, (bt_mac, start_timestamp, end_timestamp, value, value))

def get_bt_mac_list(db, table_name):
    cur = db.cursor()
    query = 'SELECT DISTINCT(bt_mac) FROM %s' % (table_name)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result
    
def get_users_list(db, table_name):
    """Get the list of users. """
    cur = db.cursor()
    query = 'SELECT DISTINCT(user) FROM %s' % (table_name)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result
    
def get_last_month_disc(db, days):
    column_names = "user\tdate\tdisc\n"
    file_name = "dataDiscoverability.tsv"

    # write to file
    cur = db.cursor()
    query = 'SELECT bt_mac, start_timestamp, value FROM %s WHERE start_timestamp > DATE_SUB(%%s, INTERVAL %s DAY)' % (TB_BLUETOOTH_DAILY, days)
    print datetime.now()
    cur.execute(query, (datetime.now()))
    fetched_data = cur.fetchall()
    cur.close()
    
    with open(file_name, 'w') as f_handle:
        f_handle.write(column_names)
        for row in fetched_data:
            # get last month data for as given bt_mac
            # wydrukuj do pliku
            filerow =  row[0] + "\t" + datetime.strftime(row[1], "%Y%m%d") + "\t" + str(row[2]) + "\n"
            f_handle.write(filerow)
   
def prepare_users_prob(db):
    users_list = get_users_list(db, DB_DATA)
    prob = {}
    day = {}
    for user in users_list:
        prob[user[0]] = 0
        day[user[0]] = False
    return (prob, day)
 
def get_last_scan_in_db(db):
    cur = db.cursor()
    query = 'SELECT id FROM %s ORDER BY id desc LIMIT 1' % (DB_DATA)
    cur.execute(query)
    fetched_data = cur.fetchall()
    cur.close()
    return fetched_data[0][0]
    
def calc_bdisc(db_data, db_qual, users_prob, user_day):
    scan_id = get_last_bluetooth_disc_scan_id(db_qual)
    last_id = get_last_scan_in_db(db_data)
    curr_id = scan_id + ITER
    
    if(curr_id >= last_id):
        curr_id = last_id
        
    while scan_id < last_id and (last_id - scan_id) > 0 :
        cur = db_data.cursor()
        query = 'SELECT timestamp, bt_mac, id FROM %s WHERE id > %s AND id < %s AND bt_mac != %s ORDER BY timestamp' % (DB_DATA, scan_id, curr_id, "-1")
        try:
            cur.execute(query)
        except:
            pass
        fetched_data = cur.fetchall()
        cur.close()
        if len(fetched_data) > 0:
            cal_bdisc_daily(db_data, db_qual, fetched_data, users_prob, user_day)
        else:
            "No new scans arrived."
        scan_id = curr_id
        print "Scans to go: ", last_id - scan_id
        curr_id = scan_id + ITER
        if(curr_id >= last_id):
            curr_id = last_id
        
    
def cal_bdisc_daily(db_data, db_qual, data, users_prob, user_day):
    last_timestamp = data[-1][0]
    first_timestamp = datetime(data[0][0].year, data[0][0].month, data[0][0].day, 0, 0)
    current_timestamp = first_timestamp
    idx = 0
    cur = db_qual.cursor()
    while first_timestamp < last_timestamp and idx < len(data) - 1:
        end_timestamp = first_timestamp + timedelta(days = 1)
        while current_timestamp <= end_timestamp and current_timestamp >= first_timestamp and idx < len(data) - 1:
            user = device_inventory.mapBtToUser(data[idx][1], calendar.timegm(data[idx][0].utctimetuple()), False)
            if user != None:
                insert_into_disc(db_qual, TB_BLUETOOTH_DAILY, user, first_timestamp, end_timestamp, -1)
                user_day[user] = True                 
                users_prob[user] = 0
            
            idx = idx + 1
            current_timestamp = data[idx][0]
            
        for user in user_day.keys():
            if(user_day[user] == False):
                if(users_prob[user] < DELTA):
                    insert_into_disc(db_qual, TB_BLUETOOTH_DAILY, user, first_timestamp, end_timestamp, 0)
                    users_prob[user] = users_prob[user] + 1
                else:
                    insert_into_disc(db_qual, TB_BLUETOOTH_DAILY, user, first_timestamp, end_timestamp, 1)                    
            user_day[user] = False
        first_timestamp = end_timestamp
    db_qual.commit()
    cur.close()
        
    #update last scan id
    cur.close()
    cur = db_qual.cursor()
    query = 'UPDATE bluetooth_last_scan SET scan_id = %s' % (data[-1][2])
    cur.execute(query)
    db_qual.commit()
    cur.close()    