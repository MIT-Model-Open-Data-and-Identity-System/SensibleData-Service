import calendar
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
import pandas as pd
import time
import pytz
from sklearn.cluster import DBSCAN
from questions.available_questions import dateutils
from utils import db_wrapper
from db_access.named_queries import NAMED_QUERIES


def groupwhile(df, fwhile):
        groups = []
        i = 0
        while i < len(df):
                j = i
                while j < len(df) - 1 and fwhile(i, j + 1):
                        j = j + 1
                groups.append(df.iloc[i:j + 1])
                i = j + 1
        return groups


def haversine(lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        m = 6367000 * c
        return m


def haversine_metric(a, b):
        if len(a) == 2 and len(b) == 2:
                return haversine(lon1=a[0], lat1=a[1], lon2=b[0], lat2=b[1])
        return 0


def getstops_dbscan(user, grp):
        group_dist = 60
        dbscan_dist = 60
        min_deltat = 1

        groups = groupwhile(grp, lambda start, next: haversine(grp['lon'].values[start],
                                                               grp['lat'].values[start], grp['lon'].values[next],
                                                               grp['lat'].values[next]) <= group_dist)
        values = []
        for g in groups:
                values.append([user, g.lon.median(), g.lat.median(), g.timestamp.values[0], g.timestamp.values[-1]])
        stops = pd.DataFrame(values, columns=['user', 'lon', 'lat', 'arrival', 'departure'])
        stops = stops[stops.departure - stops.arrival >= min_deltat]

        if len(stops) > 0:
                X = stops[['lon', 'lat']].values
                db = DBSCAN(dbscan_dist, min_samples=1, metric=haversine_metric).fit(X)
                stops['label'] = db.labels_
                return stops
        else:
                return None


def get_users(db, role):
        rows = db.execute_named_query(NAMED_QUERIES['get_unique_users_locationprobe_'+role], None)
        allusers = [d['user'] for d in rows.fetchall()]
        return allusers


def dorun(role):
        print 'starting'
        db = db_wrapper.DatabaseHelper()
        users = get_users(db, role)
        for iu, uid in enumerate(users):
                print ('%d/%d') % (iu,len(users))
                startt = time.time()
                db.execute_named_query(NAMED_QUERIES['delete_stops_'+role], (uid,), readonly=False)
                page = 0
                rows = []
                while True:
                        cur = db.retrieve({'limit': 100000,
                                           'after': page,
                                           'fields': ['timestamp', 'lon', 'lat'],
                                           'users': [uid]},
                                          'resampled_location',
                                          roles=[role]
                        )
                        newrows = [r for r in cur]
                        if len(newrows) == 0:
                                break
                        rows.extend(newrows)
                        page += 1
                if len(rows) > 0:
                        epoch = [dateutils.mysql_datetime_to_epoch(r['timestamp']) for r in rows]
                        df = pd.DataFrame(rows)
                        df['timestamp'] = epoch
                        stops = getstops_dbscan(uid, df)
                        if stops is not None:
                                stops['timestamp'] = [dateutils.epoch_to_mysql_string(t) for t in stops.arrival]
                                db.insert_rows(stops.to_dict(outtype='records'),
                                               'question_stop_locations',
                                               roles=[role])
                                print '%s: found %d stops in %ds' % (uid, len(stops), int(time.time() - startt))
        print 'done'

NAME = 'stops_question'


def stops_answer(request, user, scopes, users_to_return, user_roles, own_data):
        now = time.time()
        page = request.GET.get('page', 0)
        start_date = request.GET.get('start_date', 0)
        end_date = request.GET.get('end_date', now)
        db = db_wrapper.DatabaseHelper()
        print page
        cur = db.retrieve({'limit': 100,
                           'after': page,
                           'fields': ['arrival', 'departure', 'lon', 'lat', 'label'],
                           'start_date': float(start_date),
                           'end_date': float(end_date),
                           'users': [user],
                           'sortby': 'timestamp',
                          },
                          'question_stop_locations',
                          roles=user_roles
        )
        rows = [r for r in cur]
        print 'fetched %d in %ds' % (len(rows), int(time.time() - now))
        return rows
