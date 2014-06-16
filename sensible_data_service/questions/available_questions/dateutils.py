import calendar
import pytz
from datetime import datetime


_cet = pytz.timezone('CET')
_MYSQL_DATETIME_STRF = '%Y-%m-%d %H:%M:%S'


def mysql_datetime_to_epoch(dt):
        return calendar.timegm(_cet.localize(dt).utctimetuple())


def epoch_to_mysql_string(t):
        return pytz.utc.localize(
                datetime.utcfromtimestamp(t)).astimezone(_cet).strftime(_MYSQL_DATETIME_STRF)


def datetime_to_string(dt):
        return dt.strftime(_MYSQL_DATETIME_STRF)
