from pymongo import MongoClient
from sensible_data_service.sensible_data_service import LOCAL_SETTINGS


class AuditDB:

    def __init__(self, **options):
        self.database_name = LOCAL_SETTINGS.AUDIT_DATABASE['DATABASE']
        self.host = LOCAL_SETTINGS.AUDIT_DATABASE['HOST']
        self.port = LOCAL_SETTINGS.AUDIT_DATABASE['PORT']
        self.username = LOCAL_SETTINGS.AUDIT_DATABASE['USERNAME']
        self.password = LOCAL_SETTINGS.AUDIT_DATABASE['PASSWORD']
        self.collection_name = LOCAL_SETTINGS.AUDIT_DATABASE['COLLECTION']
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

    def get_accesses(self, username):
        query = {}

        # when researchers have accessed a user in particular or all of them
        query['users'] = {'$in': [username, 'all']}

        return self.collection.find(query)

