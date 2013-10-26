from django.core.management.base import NoArgsCommand
from authorization_manager import authorization_manager
from authorization_manager.models import Authorization
from application_manager.models import Application, GcmRegistration
from collections import defaultdict
import json
import time
from utils import database
from application_manager import gcm_server
from connectors.connector_facebook import auth

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		user_auths = defaultdict(lambda: defaultdict(int))
		authorizations = Authorization.objects.filter(application=Application.objects.get(connector_type='facebook_in'), active=True)
		db = database.Database()
		inventory = list()
		now = time.time()
		for a in authorizations:
			user = a.user
			expires_at = json.loads(a.payload)['expires_at']
			if expires_at < now:
				a.active = False
				a.save()
