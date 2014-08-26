from pymongo import MongoClient
from sensible_data_service import LOCAL_SETTINGS
from utils import SECURE_settings
from datetime import datetime, date, timedelta, time
from dateutil.relativedelta import relativedelta

class AuditDB:

    def __init__(self, **options):
        self.database_name = LOCAL_SETTINGS.AUDIT_DATABASE['DATABASE']
        self.host = LOCAL_SETTINGS.AUDIT_DATABASE['HOST']
        self.port = LOCAL_SETTINGS.AUDIT_DATABASE['PORT']
        self.username = SECURE_settings.AUDIT_DATABASE['USERNAME']
        self.password = SECURE_settings.AUDIT_DATABASE['PASSWORD']
        self.collection_name = LOCAL_SETTINGS.AUDIT_DATABASE['COLLECTION']
        self.day_user_agg_name = LOCAL_SETTINGS.AUDIT_DATABASE['DAILY_USER_AGG_COLLECTION']
        self.week_user_agg_name = LOCAL_SETTINGS.AUDIT_DATABASE['WEEKLY_USER_AGG_COLLECTION']
        self.day_researcher_agg_name = LOCAL_SETTINGS.AUDIT_DATABASE['DAILY_RESEARCHER_AGG_COLLECTION']
        self.week_researcher_agg_name = LOCAL_SETTINGS.AUDIT_DATABASE['WEEKLY_RESEARCHER_AGG_COLLECTION']
        self.stats_name = LOCAL_SETTINGS.AUDIT_DATABASE['STATS_COLLECTION']
        self.options = options
        self._connect()

    def _connect(self):
        """
            Establishes a connection to the database.
        """
        self.client = MongoClient('mongodb://%s:%s' % (self.host, self.port))
        self.database = self.client[self.database_name]
        self.authenticated = self.database.authenticate(self.username, self.password)
        self.collection = self.database[self.collection_name]

        self.day_user_agg = self.database[self.day_user_agg_name]
        self.week_user_agg = self.database[self.week_user_agg_name]
        self.day_researcher_agg = self.database[self.day_researcher_agg_name]
        self.week_researcher_agg = self.database[self.week_researcher_agg_name]
        self.stats = self.database[self.stats_name]

    def weekrange(self, start_date, end_date):
      weeks = []
      for day in self.daterange(start_date, end_date):
        w = self.year_week(day)
        if w not in weeks:
          weeks.append(w)
          yield w

    def daterange(self, start_date, end_date):
      for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

    def year_week(self, d):
      """
        Returns the given week year number, starting from January 1st being week 1.
      """
      for week in self.year_weeks(d.year):
        if week > d:
          return previous_week
        else:
          previous_week = week
      return previous_week

    def year_weeks(self, year):
      """
        Returns an interator with all the weeks for the given year.
      """
      first = datetime(year, 1, 1)
      last = datetime(year, 12, 31)
      for i in range(0, int(last.strftime('%W'))):
        yield first + timedelta(i * 7)

    def get_week(self, year, week_num):
      if week_num > int(datetime(year, 12, 31).strftime('%W')):
        return self.year_weeks(year).next()
      count = 0
      for week in self.year_weeks(year):
        if count == week_num:
          return week
        count += 1
      return week

    def get_weekly_user_accesses(self, user, year=None):
      """
      Returns the aggregated accesses to the user data by week.
      If *year* is not set, current year will be used.
      """
      query = {}

      if year is None:
        year = datetime.today().year

      query['_id.year'] = year
      query['_id.user'] = user
      results = self.week_user_agg.find(query)
      cleaned = []
      for result in results:
        clean = {'researcher' : result['_id']['researcher'], 'week': result['_id']['week'],
          'year' : result['_id']['year'], 'accesses' : result['value']['accesses'],
          'requests' : result['value']['requests']}
        cleaned.append(clean)
      return {'meta' : {'year': year}, 'results' : cleaned}

    def get_weekly_researcher_accesses(self, year=None):
      """
      Returns the aggregated accesses to the user data by week.
      If *year* is not set, current year will be used.
      """
      query = {}

      if year is None:
        year = datetime.today().year

      query['_id.year'] = year
      results = self.week_researcher_agg.find(query)
      return {'meta' : {'year': year}, 'results' : results}

    def get_raw_accesses(self, user, researcher, week=None, year=None):
      """
      Returns the aggregated accesses to the user data by day for one week.
      """
      today = datetime.today()
      day = datetime.today()
      if year is not None and week is not None:
        day = self.year_week(day)
      if year is None: year = day.year
      if week is not None:
        day = self.get_week(year, week)
      if week is None:
        day = self.year_week(day)

      next_week_day = self.year_week(day + timedelta(7))

      query = {}
      query['time'] = {'$gte' : day, '$lt' : next_week_day}
      query['researcher'] = researcher
      query['accesses.user'] = {'$in' : [user]} #user
      results = self.collection.find(query, {'_id' : 0})
      cleaned_results = []
      for result in results:
        clean = result.copy()
        del clean['researcher']
        for access in result['accesses']:
          if access['user'] == user:
            clean['count'] = access['count']
            break
        del clean['accesses']
        cleaned_results.append(clean)

      return {'meta' : {'day' : query['time'], 'year': year, 'week' : week}, 'results' : cleaned_results}

    def get_user_accesses(self, user, week=None, year=None):
      """
      Returns the aggregated accesses to the user data by day for one week.
      """
      day = datetime.today()
      if year is not None and week is not None:
        day = self.year_week(day)
      if year is None: year = day.year
      if week is not None:
        day = self.get_week(year, week)
      if week is None:
        day = self.year_week(day)

      next_week_day = self.year_week(day + timedelta(7))

      query = {}
      query['day'] = {'$gte' : day.timetuple().tm_yday, '$lt' : next_week_day.timetuple().tm_yday}
      query['year'] = year
      query['user'] = user

      results = self.day_user_agg.find(query, {'_id' : 0})
      return {'meta' : {'day' : query['day'], 'year': year, 'week' : week}, 'results' : results}

    def get_weekly_avg_accesses(self, year=None):
      query = {}

      if year is None:
        year = datetime.today().year

      query['_id.year'] = year
      results = self.stats.find()
      return {'meta' : {'year': year}, 'results' : results}

    def get_avg_accesses(self, week=None, year=None):
      """
      Returns the aggregated accesses to the user data by day.
      If *start* is not set, one month before *end* will be used.
      If *end* is not set, current day will be used.
      """

      day = datetime.today()
      if year is not None and week is not None:
        day = self.year_week(day)
      if year is None: year = day.year
      if week is not None:
        day = self.get_week(year, week)
      if week is None:
        day = self.year_week(day)

      next_week_day = self.year_week(day + timedelta(7))

      query = {}
      query['day'] = {'$gte' : day.timetuple().tm_yday, '$lt' : next_week_day.timetuple().tm_yday}
      query['year'] = day.year

      results = self.day_researcher_agg.find(query, {'_id' : 0})

      return {'meta' : {'day' : query['day'], 'year': year, 'week' : week}, 'results' : results}
