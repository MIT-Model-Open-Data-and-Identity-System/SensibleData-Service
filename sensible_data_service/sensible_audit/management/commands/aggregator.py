"""Audit Aggregator.

Usage:
  agg.py aggregate day [--start_date DATE] [--end_date DATE]
  agg.py aggregate week [--start_week WEEK] [--end_week WEEK]
  agg.py index

Options:
  -h, --help          Show this screen.
  --version           Show version.
  --start_date DATE   Start day (included) in format "YYYY/mm/dd" [default: yesterday].
  --end_date DATE     End day (excluded) in format "YYYY/mm/dd" [default: today].
  --start_week WEEK   Start week (included) in format "YYYY/dd" [default: current_week].
  --end_week WEEK     End week (excluded) in format "YYYY/dd" [default: next_week].
"""
from pymongo import MongoClient, ASCENDING
from bson.code import Code
from bson.son import SON
from utils.SECURE_settings import AUDIT_DATABASE
import datetime
import re
import time

class Database:

  def __init__(self):
    self.host = AUDIT_DATABASE['HOST']
    self.port = AUDIT_DATABASE['PORT']
    self.username = AUDIT_DATABASE['USERNAME']
    self.password = AUDIT_DATABASE['PASSWORD']
    self.database = AUDIT_DATABASE['DATABASE']
    self.data_collection_name = AUDIT_DATABASE['COLLECTION']
    self.agg_day_user_name = AUDIT_DATABASE['COLLECTION_AGG_DAY_USER']
    self.agg_day_user_tmp_name = AUDIT_DATABASE['COLLECTION_AGG_DAY_USER'] + '.tmp'
    self.agg_day_researcher_name = AUDIT_DATABASE['COLLECTION_AGG_DAY_RESEARCHER']
    self.agg_day_researcher_tmp_name = AUDIT_DATABASE['COLLECTION_AGG_DAY_RESEARCHER'] + '.tmp'
    self.stats_name = AUDIT_DATABASE['COLLECTION_DAY_STATS']

    self.agg_week_user_name = AUDIT_DATABASE['COLLECTION_AGG_WEEK_USER']
    self.agg_week_researcher_name = AUDIT_DATABASE['COLLECTION_AGG_WEEK_RESEARCHER']

    self._connect()

  def _connect(self):
    self.client = MongoClient(self.host, self.port)

    # authenticate
    self.client[self.database].authenticate(self.username, self.password)

    self.collection = self.client[self.database][self.data_collection_name]
    self.stats = self.client[self.database][self.stats_name]
    self.coll_agg_day_user = self.client[self.database][self.agg_day_user_name]
    self.coll_agg_day_user_tmp = self.client[self.database][self.agg_day_user_tmp_name]

    self.coll_agg_day_researcher = self.client[self.database][self.agg_day_researcher_name]
    self.coll_agg_day_researcher_tmp = self.client[self.database][self.agg_day_researcher_tmp_name]
    self.coll_agg_week_researcher = self.client[self.database][self.agg_week_researcher_name]

    self.coll_agg_week_user = self.client[self.database][self.agg_week_user_name]

  def ensure_index(self, collection, indexes, **options):
    print 'ensuring index "{ %s }" in collection %s ...' % (indexes, collection.name)
    collection.ensure_index(indexes, **options)


def aggregate_stats(day):
  # connect to database
  db = Database()

  print '## %s' % db.stats_name

  # next day
  next_day = datetime.datetime.combine(day + datetime.timedelta(days=1), datetime.time())

  # map reduce code
  map = Code('''function() {

    if (!this.accesses) return;

    var day = Date.UTC(this.time.getFullYear(), this.time.getMonth(), this.time.getDate());

    var key = { researcher : this.researcher, time : day};
    var value = { requests : 1};
    emit(key, value);

  }
  ''')

  reduce = Code('''
    function(key, values) {
      var reduced = {requests : 0};

      values.forEach(function(v) {
          reduced.requests += v.requests;
      });

      return reduced;
  }
  ''')

  # limit entries for this day
  query = {'time' : {'$gte' : datetime.datetime(day.year, day.month, day.day),
    '$lt' : datetime.datetime(next_day.year, next_day.month, next_day.day)}}

  start = time.time()
  # perform map reduce
  print ' => Map reduce on %s. ' % db.stats_name
  db.collection.map_reduce(map, reduce,
    out=SON([('merge', db.stats_name)]), query=query)

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

def aggregate_stats_week(week):
  # connect to database
  db = Database()

  print '## %s.week' % db.stats_name

  # map reduce code
  map = Code('''function() {

    var date = new Date(this._id.time);
    var first = new Date(date.getFullYear(), 0, 1);
    var day = Math.round(((date - first) / 1000 / 60 / 60 / 24) + .5, 0);

    var key = { researcher : this._id.researcher, week : NumberInt(day / 7), year : date.getFullYear()};
    var value = { requests : this.value.requests};
    emit(key, value);

  }
  ''')

  reduce = Code('''
    function(key, values) {
      var reduced = {requests : 0};

      values.forEach(function(v) {
          reduced.requests += v.requests;
      });

      return reduced;
  }
  ''')

  next_week_day = year_week(week + datetime.timedelta(7))

  query = {'_id.time' : {'$gte' : time.mktime(week.timetuple()) * 1000,
    '$lt' : time.mktime(next_week_day.timetuple()) * 1000}}

  start = time.time()
  # perform map reduce
  print ' => Query: %s' % query
  db.stats.map_reduce(map, reduce,
    out=SON([('merge', db.stats_name + '.week')]), query=query)

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

def aggregate_day_researcher(day):
  # connect to database
  db = Database()

  print '## %s' % db.agg_day_researcher_name + '.users'

  # next day
  next_day = datetime.datetime.combine(day + datetime.timedelta(days=1), datetime.time())

  # map reduce code
  map = Code('''function() {

    if (!this.accesses) return;

    var day = Date.UTC(this.time.getFullYear(), this.time.getMonth(), this.time.getDate(), 1, 0, 0);

    for (var access in this.accesses) {
        var key = { researcher : this.researcher, time : day, user : this.accesses[access].user };
        var value = { accesses : this.accesses[access].count};
        emit(key, value);
    }

  }
  ''')

  reduce = Code('''
    function(key, values) {
      var reduced = {accesses : 0};

      values.forEach(function(v) {
          reduced.accesses += v.accesses;
      });

      return reduced;
  }
  ''')

  # limit entries for this day
  query = {'time' : {'$gte' : datetime.datetime(day.year, day.month, day.day),
    '$lt' : datetime.datetime(next_day.year, next_day.month, next_day.day)}}

  start = time.time()
  # perform map reduce
  print ' => Map reduce on %s. ' % (db.data_collection_name)
  db.collection.map_reduce(map, reduce,
    out=SON([('replace', db.agg_day_researcher_name + '.users')]), query=query)

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

  print '## %s' % db.agg_day_researcher_name + '.accesses'

  # map reduce code
  map = Code('''function() {

    var key = { researcher : this._id.researcher, time : this._id.time};
    var value = { users : 1, accesses : this.value.accesses};
    emit(key, value);

  }
  ''')

  reduce = Code('''
    function(key, values) {
      var reduced = {accesses : 0, users : 0};

      values.forEach(function(v) {
          reduced.accesses += v.accesses;
          reduced.users += v.users;
      });

      return reduced;
  }
  ''')

  start = time.time()
  # perform map reduce
  print ' => Map reduce on %s. ' % db.agg_day_researcher_name + '.users'
  db.client[db.database][db.agg_day_researcher_name + '.users'].map_reduce(map, reduce,
    out=SON([('replace', db.agg_day_researcher_name + '.accesses')]))

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

  pipe = []
  print ' => Aggregate results to %s. ' % db.agg_day_researcher_name

  pipe.append({ "$group" : { "_id" : { 'researcher' : '$_id.researcher',
    'time' : '$_id.time'}, "accesses" : {"$sum" : "$value.accesses"},
    "users" : {"$sum" : "$value.users"}}})

  pipe.append({ "$project" : { "date" : { "$add" : [datetime.datetime(1970, 1,1), "$_id.time"]},
    "researcher" : "$_id.researcher", "accesses" : 1, "users" : 1, "_id" : 0}})
  pipe.append({'$project' : {"researcher" : 1, "day" : {"$dayOfYear" : "$date"},
    "year" : {"$year" : "$date"}, "accesses" : 1, "users" : 1}})

  db.coll_agg_day_researcher.remove({'day' : int(datetime.datetime.strftime(day, "%j")),
    'year' : int(datetime.datetime.strftime(day, "%Y"))})
  start = time.time()
  results = db.client[db.database][db.agg_day_researcher_name + '.accesses'].aggregate(pipe)['result']
  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)
  if len(results) > 0: db.coll_agg_day_researcher.insert(results)

def aggregate_day_user(day):
  # connect to database
  db = Database()

  print '## %s' % db.agg_day_user_name

  # next day
  next_day = datetime.datetime.combine(day + datetime.timedelta(days=1), datetime.time())

  # map reduce code
  map = Code('''function() {

    var day = Date.UTC(this.time.getFullYear(), this.time.getMonth(), this.time.getDate(), 1, 0, 0);

    if (!this.accesses) return;
    for (var access in this.accesses) {
        var key = { user : this.accesses[access].user, date : day,
          probe : this.probe, researcher : this.researcher};
        var value = { accesses : this.accesses[access].count, requests : 1};
        emit(key, value);
    }

  }
  ''')

  reduce = Code('''
    function(key, values) {
      var reduced = {accesses : 0, requests : 0};

      values.forEach(function(v) {
          reduced.accesses += v.accesses;
          reduced.requests += v.requests;
      });

      return reduced;
  }
  ''')

  # limit entries for this day
  query = {'time' : {'$gte' : datetime.datetime(day.year, day.month, day.day),
    '$lt' : datetime.datetime(next_day.year, next_day.month, next_day.day)}}

  # drop current collection
  print ' => Drop collection %s. ' % db.agg_day_user_tmp_name
  db.coll_agg_day_user_tmp.drop()

  start = time.time()
  # perform map reduce
  print ' => Map reduce on %s. ' % db.agg_day_user_tmp_name
  db.collection.map_reduce(map, reduce,
    out=SON([('replace', db.agg_day_user_tmp_name)]), query=query)

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

  print ' => Aggregate results to %s. ' % db.agg_day_user_name
  db.coll_agg_day_user.remove({'day' : int(datetime.datetime.strftime(day, "%j")),
    'year' : int(datetime.datetime.strftime(day, "%Y"))})

  pipe = []
  pipe.append({ '$group' : { "_id" : { "_id" : "$_id", "user" : "$_id.user",
    "researcher" : "$_id.researcher", "probe" : "$_id.probe",
    "date" : "$_id.date"},
    "accesses" : {"$sum" : "$value.accesses"}, "requests" : {"$sum" : "$value.requests"}}})

  pipe.append({'$group' : { "_id" : {"user" : "$_id.user", "date" : "$_id.date"},
   "researchers" : {"$push" : {"researcher" : "$_id.researcher",
   "accesses" : "$accesses", "requests" : "$requests", "probe" : "$_id.probe"}}}})

  pipe.append({'$project' : {"user" : "$_id.user",
    "date" : { "$add" : [datetime.datetime(1970, 1,1), "$_id.date"]},
     "researchers" : "$researchers", "_id" : 0}})

  pipe.append({'$project' : {"user" : "$user", "day" : {"$dayOfYear" : "$date"},
   "year" : {"$year" : "$date"}, "researchers" : "$researchers", "_id" : 0}})

  start = time.time()
  results = db.coll_agg_day_user_tmp.aggregate(pipe)['result']
  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)
  if len(results) > 0: db.coll_agg_day_user.insert(results)
  db.coll_agg_day_user_tmp.drop()

def aggregate_week_researcher(week):

  # connect to database
  db = Database()

  print '## %s' % db.agg_week_researcher_name

  map = Code('''
  function() {

    var date = new Date(this.year, 0);
    var dayOfYear = new Date(date.setDate(this.day));

    var first = new Date(this.year, 0, 1);
    var day = Math.round(((dayOfYear - first) / 1000 / 60 / 60 / 24) + .5, 0);

    var week = Math.floor(day / 7);
    if (day % 7 == 0)
      week = week - 1;

    var key = {researcher : this.researcher,
      week : NumberInt(week), year : NumberInt(this.year)};
    var value = { accesses : this.accesses, users : this.users};
    emit(key, value);
  }
  ''')

  reduce = Code('''
  function(key, values) {
    reduced = { accesses : 0, users : 0};
    for (var idx = 0; idx < values.length; idx++) {
        reduced.accesses += values[idx].accesses;
        reduced.users += values[idx].users;
    }
    return reduced;
  }
  ''')

  next_week_day = year_week(week + datetime.timedelta(8))

  if next_week_day.timetuple().tm_yday < week.timetuple().tm_yday:
    query = {'$or' : [
      {'day' : {'$gte' : week.timetuple().tm_yday, '$lt' : 366}, 'year' : week.year},
      {'day' : {'$gte' : 1, '$lt' : next_week_day.timetuple().tm_yday}, 'year' : week.year}]}
  else:
    query = {'day' : {'$gte' : week.timetuple().tm_yday,
      '$lt' : next_week_day.timetuple().tm_yday}, 'year' : week.year}

  start = time.time()
  # perform map reduce
  print ' => Query: %s' % query
  db.coll_agg_day_researcher.map_reduce(map, reduce,
    out=SON([('merge', db.agg_week_researcher_name)]), query=query)

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

def aggregate_week_user(week):
  # connect to database
  db = Database()

  print '## %s' % db.agg_week_user_name

  map = Code('''
  function() {

      var date = new Date(this.year, 0);
      var dayOfYear = new Date(date.setDate(this.day));

      var first = new Date(this.year, 0, 1);
      var day = Math.round(((date - first) / 1000 / 60 / 60 / 24) + .5, 0);

      var week = Math.floor(day / 7);
      if (day % 7 == 0)
        week = week - 1;

      if (this.researchers) {
        for (var idx = 0; idx < this.researchers.length; idx++) {
          var key = { user : this.user, researcher : this.researchers[idx].researcher,
            week : NumberInt(week), year : NumberInt(this.year)};
          var value = { accesses : this.researchers[idx].accesses,
            requests : this.researchers[idx].requests };
          emit (key, value);
        }
      }
  }
  ''')

  reduce = Code('''
  function(key, values) {
    reduced = { accesses : 0, requests : 0};
    for (var idx = 0; idx < values.length; idx++) {
        reduced.accesses += values[idx].accesses;
        reduced.requests += values[idx].requests;
    }
    return reduced;
  }
  ''')

  next_week_day = year_week(week + datetime.timedelta(8))

  if next_week_day.timetuple().tm_yday < week.timetuple().tm_yday:
    query = {'$or' : [
      {'day' : {'$gte' : week.timetuple().tm_yday, '$lt' : 366}, 'year' : week.year},
      {'day' : {'$gte' : 1, '$lt' : next_week_day.timetuple().tm_yday}, 'year' : week.year}]}
  else:
    query = {'day' : {'$gte' : week.timetuple().tm_yday,
      '$lt' : next_week_day.timetuple().tm_yday}, 'year' : week.year}

  start = time.time()
  print ' => Query: %s' % query

  db.coll_agg_day_user.map_reduce(map, reduce,
    out=SON([('merge', db.agg_week_user_name)]), query=query)

  end = time.time()
  print ' => Completed. Took %s seconds.\n' % (end - start)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

def weekrange(start_date, end_date):
  weeks = []
  for day in daterange(start_date, end_date):
    w = year_week(day)
    if w not in weeks:
      weeks.append(w)
      yield w

def year_week(d):
  """
    Returns the given week year number, starting from January 1st being week 1.
  """
  for week in year_weeks(d.year):
    if week > d:
      return previous_week
    else:
      previous_week = week
  return previous_week

def year_weeks(year):
  """
    Returns an interator with all the weeks for the given year.
  """
  first = datetime.datetime(year, 1, 1)
  last = datetime.datetime(year, 12, 31)
  for i in range(0, int(last.strftime('%W'))):
    yield first + datetime.timedelta(i * 7)

def validate_week(date_str):
  if date_str == 'next_week':
    return year_week(datetime.datetime.combine(datetime.date.today() +
      datetime.timedelta(days=7), datetime.time()))
  elif date_str == 'current_week':
    return year_week(datetime.datetime.today())
  try:
      return parseweek(date_str)
  except AttributeError, e:
    print e
    return 0

def parseweek(date_str):
  m = re.match(r'(\d{4})/(\d{1,2})', date_str)
  if m:
    year = int(m.group(1))
    week_num = int(m.group(2))
    if week_num > int(datetime.datetime(year, 12, 31).strftime('%W')):
      raise ValueError('Date format %s not correct (YYYY/dd).' % date_str)
    count = 0
    for week in year_weeks(year):
      if count == week_num:
        return week
      count += 1
    return week
  else:
    raise ValueError('Date format %s not correct (YYYY/dd).' % date_str)

def validate_date(date_str):
  if date_str == 'yesterday':
    return datetime.datetime.combine(datetime.date.today() -
      datetime.timedelta(days=1), datetime.time())
  elif date_str == 'today':
    return datetime.datetime.today()
  try:
    return datetime.datetime.strptime(date_str, '%Y/%m/%d')
  except ValueError, e:
    print 'Date format %s not correct (YYYY/mm/dd).' % date_str
    return False

def ensure_indexes():
  db = Database()
  db.ensure_index(db.collection, [('researcher', ASCENDING)])
  db.ensure_index(db.collection, [('time', ASCENDING)])
  db.ensure_index(db.coll_agg_day_user, [('user', ASCENDING), ('day', ASCENDING), ('year', ASCENDING)], sparse=True)
  db.ensure_index(db.coll_agg_day_user, [('day', ASCENDING), ('year', ASCENDING)])
  db.ensure_index(db.coll_agg_day_user, [('user', ASCENDING)])
  db.ensure_index(db.coll_agg_day_researcher, [('researcher', ASCENDING), ('day', ASCENDING), ('year', ASCENDING)], sparse=True)
  db.ensure_index(db.coll_agg_day_researcher, [('day', ASCENDING), ('year', ASCENDING)])
  db.ensure_index(db.coll_agg_day_researcher, [('researcher', ASCENDING)])

  db.ensure_index(db.coll_agg_week_user, [('_id.user', ASCENDING), ('_id.day', ASCENDING), ('_id.year', ASCENDING)], sparse=True)
  db.ensure_index(db.coll_agg_week_researcher, [('_id.researcher', ASCENDING), ('_id.day', ASCENDING), ('_id.year', ASCENDING)], sparse=True)
