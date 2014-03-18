from pymongo import MongoClient
from bson.code import Code
import SECURE_settings


class AuditDB:

    def __init__(self, **options):
        self.database_name = SECURE_settings.AUDIT_DATABASE['DATABASE']
        self.host = SECURE_settings.AUDIT_DATABASE['HOST']
        self.port = SECURE_settings.AUDIT_DATABASE['PORT']
        self.username = SECURE_settings.AUDIT_DATABASE['USERNAME']
        self.password = SECURE_settings.AUDIT_DATABASE['PASSWORD']
        self.collection_name = SECURE_settings.AUDIT_DATABASE['COLLECTION']
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


    def get_accesses_by_researcher(self, username):
        query = {}
        query['key'] = {'user': 1, 'sys_module': 1}
        query['cond'] = {'results': {'$in': [username]}}
        query['reduce'] = Code("""function (curr, res) {}""")
        query['initial'] = {}

        return self.collection.group(key=query['key'], condition=query['cond'], 
            initial=query['initial'], reduce=query['reduce'])

    def get_accesses(self, username):
        query = {}

        # when researchers have accessed a user in particular or all of them
        query['users'] = {'$in': [username, 'all']}

        return self.collection.find(query)

