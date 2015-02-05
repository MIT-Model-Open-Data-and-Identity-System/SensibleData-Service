import time

import pandas as pd
from questions.available_questions import dateutils
from sensible_audit import audit
from utils import db_wrapper
from db_access.named_queries.named_queries import NAMED_QUERIES


log = audit.getLogger(__name__)

NAME = "resampled_location"
def recalculate(start, end, role):
        log.debug({'type': 'resampled_location', 'message': 'starting'})
        db = db_wrapper.DatabaseHelper()
        current = start
        DELTAT = 24*60*60
        t = time.time()
        while current < end:
                db.execute_named_query(NAMED_QUERIES['delete_resampled_location_' + role],
                                       (dateutils.epoch_to_mysql_string(current),
                                        dateutils.epoch_to_mysql_string(current + DELTAT)),
                                       readonly=False)
                rows = []
                page = 0
                while True:
                        cur = db.retrieve({'limit': 100000,
                                           'start_date': current,
                                           'end_date': current + DELTAT,
                                           'after': page,
                                           'fields': ['timestamp', 'lon', 'lat', 'user'],
                                           'sortby': 'timestamp'},
                                          'edu_mit_media_funf_probe_builtin_LocationProbe',
                                          roles=[role]
                        )
                        newrows = [r for r in cur]
                        if len(newrows) == 0:
                                break
                        rows.extend(newrows)
                        page += 1

                log.debug({'type': 'resampled_location',
                           'message': 'fetched %d (%d rows/s)' % (len(rows), len(rows)/(time.time() - t))})

                if len(rows) > 0:
                        alllocs = pd.DataFrame(rows)
                        resampled_rows = []
                        for uid, grp in alllocs.groupby('user'):
                                resampled = grp.drop('user',1).set_index('timestamp').resample('15min', how='median').dropna()
                                resampled['user'] = uid
                                resampled['timestamp'] = resampled.index
                                resampled['timestamp'] = resampled['timestamp'].apply(dateutils.datetime_to_string)
                                resampled_rows.extend(resampled.to_dict(outtype='records'))
                        db.insert_rows(resampled_rows, 'resampled_location', roles=[role])
                current += DELTAT

        log.debug({'type': 'resampled_location',
                                           'message': 'done in %ds' % (int(time.time() - t))})


def run_all(role):
        # from 1 Sep 2013 to today
        recalculate(1377986400, int(time.time()), role)


def run_incremental(role):
        # recalculate last week
        now = int(time.time())
        recalculate(now - 7*24*60*60, now, role)


def run():
        for role in ['researcher','developer','main']:
                run_incremental(role)

def resampled_location(request, user, scopes, users_to_return, user_roles, own_data):
        page = request.GET.get('page', 0)
        start_date = request.GET.get('start_date', 0)
        end_date = request.GET.get('end_date', time.time())

        try:
                limit = int(request.GET.get('limit', 1000))
                if limit <= 0 or limit > 1000:
                        limit = 1000
        except:
                limit = 1000

        roles_to_use = []
        if own_data and 'researcher' in user_roles: roles_to_use = ['researcher']
        if own_data and 'developer' in user_roles: roles_to_use = ['developer']
        db = db_wrapper.DatabaseHelper()
        cur = db.retrieve({'limit': limit,
                           'after': page,
                           'fields': ['user', 'lon', 'lat', 'timestamp'],
                           'start_date': float(start_date),
                           'end_date': float(end_date),
                           'users': users_to_return,
                           'sortby': 'timestamp',
                          },
                          'resampled_location',
                          roles=roles_to_use
        )
        #rows = [r for r in cur]
        rows = []
	for result in cur:
		if 'timestamp' in result:
			result['timestamp'] = int(time.mktime(result['timestamp'].timetuple()))
		rows.append(result) 
	return rows

