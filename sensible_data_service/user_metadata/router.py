class UserMetadataDatabaseRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'user_metadata':
            return 'user_metadata'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'user_metadata':
            return 'user_metadata'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'user_metadata' and \
           obj2._meta.app_label == 'user_metadata':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if model._meta.app_label in ['south']:
            return True
        if db == 'user_metadata':
            return model._meta.app_label == 'user_metadata'
        elif model._meta.app_label == 'user_metadata':
            return False
        return None

    def allow_migrate(self, db, model):
        return self.allow_syncdb(db, model)