from django.contrib.auth.models import User
from db_access.named_queries.named_queries import NAMED_QUERIES
from utils import db_wrapper

db_helper = db_wrapper.DatabaseHelper()

def populate_user_metadata():
	users = [user.username for user in User.objects.all() if not hasattr(user, "userrole")]
	facebook_ids = db_helper.execute_named_query(NAMED_QUERIES['get_facebook_ids'], ())

