from django.core.management.base import NoArgsCommand
from authorization_manager.models import Authorization
from application_manager.models import Application
import json
import time

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		authorizations = Authorization.objects.filter(application=Application.objects.get(connector_type='facebook_in'), active=True)
		now = time.time()
		for authorization in authorizations:
			expires_at = json.loads(authorization.payload)['expires_at']
			if expires_at < now:
				authorization.active = False
				authorization.save()
