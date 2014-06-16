import pandas as pd
from questions.available_questions import dateutils
from sensible_audit import audit
from utils import db_wrapper
from db_access.named_queries import NAMED_QUERIES
import time


log = audit.getLogger(__name__)


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
                                log.debug({'type': 'resampled_location',
                                           'message': 'resampled (%.1f%%)' % (100. * len(resampled) / len(grp))})
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
