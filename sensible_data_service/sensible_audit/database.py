from pymongo import MongoClient
from sensible_data_service import LOCAL_SETTINGS
from utils import SECURE_settings
from datetime import datetime
from dateutil.relativedelta import relativedelta

class AuditDB:

    def __init__(self, **options):
        self.database_name = LOCAL_SETTINGS.AUDIT_DATABASE['DATABASE']
        self.host = LOCAL_SETTINGS.AUDIT_DATABASE['HOST']
        self.port = LOCAL_SETTINGS.AUDIT_DATABASE['PORT']
        self.username = SECURE_settings.AUDIT_DATABASE['USERNAME']
        self.password = SECURE_settings.AUDIT_DATABASE['PASSWORD']
        self.collection_name = LOCAL_SETTINGS.AUDIT_DATABASE['COLLECTION']
        self.ssl = LOCAL_SETTINGS.AUDIT_DATABASE['SSL']
	self.options = options
        self._connect()

    def _connect(self):
        """
            Establishes a connection to the database.
        """
        self.client = MongoClient('mongodb://%s:%s' % (self.host, self.port), ssl=self.ssl)
        self.database = self.client[self.database_name]
        self.authenticated = self.database.authenticate(self.username, self.password)
        self.collection = self.database[self.collection_name]


    def get_agg_accesses_researcher_for_user(self, user, start_time = None):

        if start_time is None:
            start_time = datetime.today() - relativedelta(months = 1)

        pipe = []

        # limit the results to the past month
        pipe.append({"$match" : { "time" : { "$gte" : start_time }}})
        # unwind accesses to be able to find the ones we are interested in
        pipe.append({"$unwind" : "$accesses"})
        # format the result
        pipe.append({"$project" : {"researcher" : "$user", "user" : "$accesses.user", "accesses" : "$accesses.count",
            "probe" : "$probe", "date" : { "y": { "$year": "$time" }, "d": {"$dayOfYear" : "$time" }}}})
        # WHERE user = requester
        pipe.append({ "$match" : { "user" : user }})
        # sum the number of accesses per API call
        pipe.append({ "$group" : { "_id" : { "_id" : "$_id", "researcher" : "$researcher",
            "date" : "$date", "probe" : "$probe"}, "count" : { "$sum" : "$accesses"}}})
        # group by researcher, and sum the number of accesses and count the number of API call
        pipe.append({ "$group" : { "_id" : { "researcher" : "$_id.researcher", "date" : "$_id.date",
            "probe" : "$_id.probe" }, "requestCount" : { "$sum" : 1 }, "dataCount" : { "$sum" : "$count" }}})
        # format the final result
        pipe.append({ "$project" : { "researcher" : "$_id.researcher", "date" : "$_id.date",
            "probe" : "$_id.probe", "requestCount" : 1, "dataCount" : 1, "_id" : 0 }})

        return self.collection.aggregate(pipe)

    def get_agg_accesses_researcher(self, start_time = None):

        if start_time is None:
            start_time = datetime.today() - relativedelta(months = 1)

        pipe = []

        # limit the results to the past month
        pipe.append({"$match" : { "time" : { "$gte" : start_time }}})
        # unwind accesses to be able to find the ones we are interested in
        pipe.append({"$unwind" : "$accesses"})
        # format the result
        pipe.append({"$project" : {"researcher" : "$user", "user" : "$accesses.user",
            "probe": "$probe", "accesses" : "$accesses.count",
            "date" : { "y": { "$year": "$time" }, "d": {"$dayOfYear" : "$time" }}}})
        # WHERE user = requester
        #pipe.push({ "$match" : { "user" : { "$ne": user }}})
        # sum the number of accesses per API call
        pipe.append({ "$group" : { "_id" : { "_id" : "$_id", "researcher" : "$researcher", "date" : "$date",
            "probe" : "$probe" }, "count" : { "$sum" : "$accesses"}, "users" : { "$sum" : 1 }}})
        # group by researcher, and sum the number of accesses and count the number of API call
        pipe.append({ "$group" : { "_id" : { "researcher" : "$_id.researcher", "date" : "$_id.date",
            "probe" : "$_id.probe" }, "requestCount" : { "$sum" : 1 },
            "dataCount" : { "$sum" : "$count" }, "users" : { "$sum" : "$users" }}})

        # format the final result
        pipe.append({ "$project" : { "researcher" : "$_id.researcher", "date" : "$_id.date",
            "probe" : "$_id.probe", "requestCount" : 1, "dataCount" : 1, "users" : 1,  "_id" : 0 }})

        return self.collection.aggregate(pipe)
