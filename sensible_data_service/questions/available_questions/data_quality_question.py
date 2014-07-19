"""
The data quality question computes the quality of data collected within Sensible DTU project.

In order to run the question, start django shell and then type following commands:

>>> from questions import tasks
>>> run("data_quality_question") 

Author: Magdalena Furman s110848
"""

from datetime import timedelta
from datetime import datetime
from utils import SECURE_settings
from sensible_data_service import LOCAL_SETTINGS
import json
import MySQLdb

# Name of the question
NAME = 'data_quality_question'

# Name of the databases to recalculate
COLLECTIONS = {'edu_mit_media_funf_probe_builtin_BluetoothProbe' : 'bluetooth'}

#COLLECTIONS = {'edu_mit_media_funf_probe_builtin_BluetoothProbe' : 'bluetooth',
#           'edu_mit_media_funf_probe_builtin_LocationProbe'  : 'location',
#           'edu_mit_media_funf_probe_builtin_WifiProbe'      : 'wifi'}

# Quality settings
MONTH_EXP = 8640.0
WEEK_EXP = 2016.0
HOUR_EXP = 12.0
DAY_EXP = 288.0
MAX_GRADE = 1.0

# Names of tables in DB
TB_QUALITY_DAILY = 'data_quality_daily'
TB_QUALITY_HOURLY = 'data_quality_hourly'
TB_LAST_SCANS = 'user_last_scans'
TB_STATS_HOURLY = 'stats_hourly'
TB_STATS_DAILY = 'stats_daily'

# Name of quality database
DB_QUALITY = 'data_quality'

# Name of data database
#DB_DATA = 'researcher'
DB_DATA = 'main'

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

        users_list = get_users_list(db_data, DB_DATA)
        user_idx = 0
        before = datetime.now()

        for single_user in users_list:
            user_idx = user_idx + 1
            user_name = "user" + str(user_idx)
            print 'Processing ', user_name
            update_qualities(db_data, db_quality, single_user[0], COLLECTIONS[connection])
        print 'Execution time: ', datetime.now() - before
        db_data.close()
    db_quality.close()

def get_data_stats(request, users, data_type, output_type):
    """Get the statistics of data.

    Keyword arguments:
    request -- url request
    users -- the array of users, if input 'all', then the stats are computed for all users
    data_type -- type of quality, e.g. 'bluetooth', 'location' or 'wifi'
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

    if users == "all":
        users = get_users_list(db_quality, "stats_daily")

    for user in users:
        # get user stats all / month / week for quality specified as data_type
        cur = db_quality.cursor()
        query = "SELECT all_count, all_max, month_count, week_count FROM stats_daily WHERE user=%s and type=%s"
        cur.execute(query, (user[0], data_type))
        result = cur.fetchall()
        cur.close()

        if len(result) > 0:
            if result[0][0] == 0 and result[0][1] == 0:
                all_quality = 0
            else:
                all_quality = result[0][0] / float(result[0][1])

            month_quality = result[0][2] / MONTH_EXP
            week_quality = result[0][3] / WEEK_EXP

            if output_type == "json":
                results[user[0]] = {"all" : all_quality, "month" : month_quality, "week" : week_quality}
            elif output_type == "tsv":
                results = results + user[0] + "\t" + str(all_quality) + "\t" + str(month_quality) + "\t" + str(week_quality) + "\n"

    if output_type == "json":
        return json.dumps(results)
    elif output_type == "tsv":
        return results
    else:
        return ""

def get_first_last_timestamp(db, user_id, column, table_name):
    """Get first and last timestamp of a specified user. """
    cur = db.cursor()
    query = 'SELECT start_timestamp, %s FROM %s WHERE user = %%s ORDER BY start_timestamp DESC' % (column + '_quality', table_name)
    cur.execute(query, (user_id))
    fetched_data = cur.fetchall()
    cur.close()
    if len(fetched_data) == 0:
        return (None, None)
    return (fetched_data[-1][0], fetched_data[0][0])

def get_last_week_data(db, user_id, column, table_name):
    """Get the data from last week of a specified user. """
    (first_timestamp, last_timestamp) = get_first_last_timestamp(db, user_id, column, table_name)
    if(first_timestamp == None and last_timestamp == None):
        return 0
    cur = db.cursor()
    query = 'SELECT %s FROM %s WHERE user = %%s AND start_timestamp > DATE_SUB(%%s, INTERVAL 7 DAY)' % (column + '_count', table_name)
    cur.execute(query, (user_id, last_timestamp))
    fetched_data = cur.fetchall()
    quality = 0
    for item in fetched_data:
        quality = quality + item[0]
    cur.close()
    return quality

def get_last_month_data(db, user_id, column, table_name):
    """Get the data from last month of a specified user. """
    (first_timestamp, last_timestamp) = get_first_last_timestamp(db, user_id, column, table_name)
    if(first_timestamp == None and last_timestamp == None):
        return 0
    cur = db.cursor()
    query = 'SELECT %s FROM %s WHERE user = %%s AND start_timestamp > DATE_SUB(%%s, INTERVAL 37 DAY) AND start_timestamp <= DATE_SUB(%%s, INTERVAL 7 DAY)' % (column + '_count', table_name)
    cur.execute(query, (user_id, last_timestamp, last_timestamp))
    fetched_data = cur.fetchall()
    cur.close()
    quality = 0
    for item in fetched_data:
        quality = quality + item[0]
    cur.close()
    return quality

def insert_into_qual(db, table_name, user, start_timestamp, end_timestamp, column, grade, count):
    """Insert data into data quality database."""
    cur = db.cursor()
    query = 'INSERT INTO %s (user, start_timestamp, end_timestamp, bluetooth_quality, wifi_quality, location_quality, bluetooth_count, wifi_count, location_count) ' % table_name
    if column == 'bluetooth':
        query = query + 'VALUES (%s, %s, %s, %s, 0, 0, %s, 0, 0) '
    elif column == 'location':
        query = query + 'VALUES (%s, %s, %s, 0, 0, %s, 0, 0, %s) '
    elif column == 'wifi':
        query = query + 'VALUES (%s, %s, %s, 0, %s, 0, 0, %s, 0) '

    query = query + 'ON DUPLICATE KEY UPDATE %s = %s + %%s, %s = %s + %%s ' % (column + '_quality', column + '_quality', column + '_count', column + '_count')
    cur.execute(query, (user, start_timestamp, end_timestamp, grade, count, grade, count))

def get_user_last_scan_id(db, user_id, column_name):
    """Get last scan id of a specified user. """
    cur = db.cursor()
    query = "SELECT %s FROM user_last_scans WHERE user=%%s" % (column_name + '_id')
    cur.execute(query, (user_id))
    result = cur.fetchall()
    cur.close()
    if len(result) == 0: # there's no such user in the db for last scans, need to add a new row
        cur = db.cursor()
        query = 'INSERT INTO user_last_scans (user, bluetooth_id, wifi_id, location_id) VALUES (%s, 0, 0, 0)'
        cur.execute(query, (user_id))
        db.commit()
        cur.close()
        return 0
    return result[0][0]

def get_users_list(db, table_name):
    """Get the list of users. """
    cur = db.cursor()
    query = 'SELECT DISTINCT(user) FROM %s' % (table_name)
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result

def update_qualities(db, db_qual, user_id, column_name):
    """Calculate the qualitie of a specified user. """
    scan_id = get_user_last_scan_id(db_qual, user_id, column_name)
    cur = db.cursor()
    query = 'SELECT DISTINCT(timestamp) FROM %s WHERE user = %%s and id > %%s ORDER BY timestamp' % (DB_DATA)
    cur.execute(query, (user_id, scan_id))
    fetched_data = cur.fetchall()
    cur.close()
    if len(fetched_data) > 0:
        print "Calculating hourly quality..."
        calc_hour_quality(db_qual, fetched_data, user_id, column_name)
        print "Calculating daily quality..."
        calc_day_quality(db_qual, fetched_data, user_id, column_name)
        cur = db.cursor()
        query = 'SELECT id FROM %s WHERE user = %%s and id > %%s ORDER BY id' % (DB_DATA)
        cur.execute(query, (user_id, scan_id))
        fetched_data = cur.fetchall()
        cur.close()
        cur = db_qual.cursor()
        query = 'UPDATE user_last_scans SET %s = %%s WHERE user = %%s' % (column_name + '_id')
        cur.execute(query, (fetched_data[-1][0], user_id))
        db_qual.commit()
        cur.close()
    else:
        print 'No new scans arrived'

def print_stats(db_qual, column):
    """Prints statistics to a file. """
    column_names = "username\tall\tmonth\tweek\n"
    file_name = "data" + column + ".tsv"

    # write to file
    with open(file_name, 'w') as f_handle:
        f_handle.write(column_names)
        users_list = get_users_list(db_qual, "stats_daily")
        for user in users_list:
            # get user stats all / month / week for quality specified as column
            cur = db_qual.cursor()
            query = "SELECT all_count, all_max, month_count, week_count FROM stats_daily WHERE user=%s and type=%s"
            cur.execute(query, (user[0], column))
            result = cur.fetchall()
            cur.close()

            if len(result) > 0:
                if result[0][0] == 0 and result[0][1] == 0:
                    all_quality = 0
                else:
                    all_quality = result[0][0] / float(result[0][1])

                month_quality = result[0][2] / MONTH_EXP
                week_quality = result[0][3] / WEEK_EXP

                row = user[0] + "\t" + str(all_quality) + "\t" + str(month_quality) + "\t" + str(week_quality) + "\n"
                f_handle.write(row)

def calc_hour_quality(db_qual, data, user_id, column):
    """Calculate the quality hourly. """
    last_timestamp = data[-1][0]
    first_timestamp = datetime(data[0][0].year, data[0][0].month, data[0][0].day, data[0][0].hour, 0)
    current_timestamp = first_timestamp
    idx = 0
    cur = db_qual.cursor()
    all_count = 0
    all_count_max = 0
    while first_timestamp < last_timestamp and idx < len(data) - 1:
        count = 0
        end_timestamp = first_timestamp + timedelta(hours = 1)
        while current_timestamp <= end_timestamp and current_timestamp >= first_timestamp and idx < len(data) - 1:
            count = count + 1
            idx = idx + 1
            current_timestamp = data[idx][0]
        grade = count / HOUR_EXP
        insert_into_qual(db_qual, TB_QUALITY_HOURLY, user_id, first_timestamp, end_timestamp, column, grade, count)
        first_timestamp = end_timestamp
        all_count = all_count + count
        all_count_max = all_count_max + HOUR_EXP
    db_qual.commit()
    cur.close()
    update_hour_stats(db_qual, user_id, column, all_count, all_count_max)

def calc_day_quality(db_qual, data, user_id, column):
    """Calculate the quality in daily. """
    last_timestamp = data[-1][0]
    first_timestamp = datetime(data[0][0].year, data[0][0].month, data[0][0].day, 0, 0)
    current_timestamp = first_timestamp
    idx = 0
    cur = db_qual.cursor()
    all_count = 0
    all_count_max = 0
    while first_timestamp < last_timestamp and idx < len(data) - 1:
        count = 0
        end_timestamp = first_timestamp + timedelta(days = 1)
        while current_timestamp <= end_timestamp and current_timestamp >= first_timestamp and idx < len(data) - 1:
            count = count + 1
            idx = idx + 1
            current_timestamp = data[idx][0]
        grade = count / DAY_EXP
        insert_into_qual(db_qual, TB_QUALITY_DAILY, user_id, first_timestamp, end_timestamp, column, grade, count)
        first_timestamp = end_timestamp
        all_count = all_count + count
        all_count_max = all_count_max + DAY_EXP
    db_qual.commit()
    cur.close()
    update_day_stats(db_qual, user_id, column, all_count, all_count_max)

def update_hour_stats(db_qual, user_id, typ, all_count, all_count_max):
    """Update hourly statistics. """
    [all_count_db, all_count_max_db] = get_stats_all(db_qual, user_id, typ, TB_STATS_HOURLY)
    all_count = all_count + all_count_db
    all_count_max = all_count_max + all_count_max_db
    month_count = get_last_month_data(db_qual, user_id, typ, TB_QUALITY_HOURLY)
    week_count = get_last_week_data(db_qual, user_id, typ, TB_QUALITY_HOURLY)
    insert_into_stats(db_qual, TB_STATS_HOURLY, user_id, typ, all_count, all_count_max, month_count, week_count)

def update_day_stats(db_qual, user_id, typ, all_count, all_count_max):
    """Update daily statistics. """
    [all_count_db, all_count_max_db] = get_stats_all(db_qual, user_id, typ, TB_STATS_DAILY)
    all_count = all_count + all_count_db
    all_count_max = all_count_max + all_count_max_db
    month_count = get_last_month_data(db_qual, user_id, typ, TB_QUALITY_DAILY)
    week_count = get_last_week_data(db_qual, user_id, typ, TB_QUALITY_DAILY)
    insert_into_stats(db_qual, TB_STATS_DAILY, user_id, typ, all_count, all_count_max, month_count, week_count)

def insert_into_stats(db, table_name, user_id, typ, all_count, all_count_max, month_count, week_count):
    """Insert statistics into database. """
    cur = db.cursor()
    query = 'INSERT INTO %s (user, type, all_count, all_max, month_count, week_count) ' % table_name
    query = query + 'VALUES (%s, %s, %s, %s, %s, %s) '
    query = query + 'ON DUPLICATE KEY UPDATE all_count = all_count + %%s, all_max = all_max + %%s, month_count = %%s, week_count = %%s ' % ()
    cur.execute(query, (user_id, typ, all_count, all_count_max, month_count, week_count, all_count, all_count_max, month_count, week_count))
    db.commit()
    cur.close()

def get_stats_all(db_qual, user_id, typ, table_name):
    """Get statistics of 'all' quality of a specified user. """
    cur = db_qual.cursor()
    query = "SELECT all_count, all_max FROM %s WHERE user=%%s and type=%%s" % (table_name)
    cur.execute(query, (user_id, typ))
    result = cur.fetchall()
    cur.close()
    if len(result) == 0:
        return [0, 0]
    return result[0]